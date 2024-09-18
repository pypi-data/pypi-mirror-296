import abc
import re
from oligopipe.entities import Variant
import gzip, zipfile, bz2, lzma
import io

from oligopipe.preprocess.annotation import Annotator


class VariantFormatParser(metaclass=abc.ABCMeta):

    _ref_alt_pattern = re.compile("^[A|C|T|G|*|-]+$")
    _chr_pattern = re.compile("^[1-9]|1[0-9]|2[0-2]|X|Y|M$")

    _chrom_pos = None
    _position_pos = None
    _ref_pos = None
    _alt_pos = None
    _zyg_pos = None

    def _create_variant(self, line, line_number, row_filter):
        row = line.split()
        if row != [''] and row_filter(row) and re.search('[a-zA-Z]', line):
            parsed_chrom = self.parse_chrom(row, self._chrom_pos, line_number)
            parsed_pos = self.parse_pos(row, self._position_pos, line_number)
            parsed_ref = self.parse_ref(row, self._ref_pos, line_number)
            parsed_alt_list = self.parse_alt(row, self._alt_pos, line_number)
            parsed_zygosity = self.parse_zygosity(row, self._zyg_pos, line_number)
            return Variant(parsed_chrom, parsed_pos, parsed_ref, alt_list=parsed_alt_list, raw_zygosity=parsed_zygosity)
        else:
            raise ParsingError("Invalid format at line {0} for variant: {1}".format(line_number, line))

    @abc.abstractmethod
    def parse_zygosity(self, row, zygosity_pos, line_nb):
        raise Exception("Abstract method must be implemented")

    def parse_ref(self, row, ref_pos, line_nb):
        try:
            ref = row[ref_pos]
        except Exception:
            raise ParsingError("Unexpected number of fields at line {0}".format(line_nb))
        if not self._ref_alt_pattern.match(ref):
            raise ParsingError("Invalid format for reference at line {0}".format(line_nb))
        else:
            return ref

    @abc.abstractmethod
    def parse_alt(self, row, alt_pos, line_nb):
        raise Exception("Abstract method must be implemented")

    def parse_chrom(self, row, chrom_pos, line_nb, skip_weird_contigs=False):
        try:
            chrom = row[chrom_pos]
        except Exception:
            raise ParsingError("Unexpected number of fields at line {0}".format(line_nb))
        chrom = re.sub(r'^chr', '', chrom, count=1, flags=re.I)
        if not self._chr_pattern.match(chrom):
            if not skip_weird_contigs:
                raise ParsingError("Invalid format for chromosome at line {0}".format(line_nb))
            else:
                return 'NA'  # temporary solution, a variant is created but won't be found in the DB...
                # (because not clear how to skip without raising error TODO)
        else:
            return chrom

    def parse_pos(self, row, pos_pos, line_nb):
        try:
            pos = row[pos_pos]
        except Exception:
            raise ParsingError("Unexpected number of fields at line {0}".format(line_nb))
        try:
            return int(pos)
        except Exception:
            raise ParsingError("Invalid format for position at line {0} (must be numerical)".format(line_nb))


class DefaultVariantFormatParser(VariantFormatParser):
    _chrom_pos = 0
    _position_pos = 1
    _ref_pos = 2
    _alt_pos = 3
    _zyg_pos = 4

    def parse(self, man_input):
        lines = man_input.split("\n")
        line_count = 0
        for line in lines:
            line_count += 1
            line = line.replace('\r', '').rstrip("\n")
            if line:
                variant = self._create_variant(line, line_count, lambda row: len(row) == 5)
                if variant:
                    yield variant

    def parse_alt(self, row, alt_pos, line_nb):
        try:
            alt = row[alt_pos]
        except Exception:
            raise ParsingError("Unexpected number of fields at line {0}".format(line_nb))
        alt_list = alt.split(",")
        # in manual input we only allow one alternative allele
        if len(alt_list) > 1:
            raise ParsingError("Cannot determine alternative allele from the list of options at line {0}. "
                               "Please provide only one alternative.".format(line_nb))
        if not self._ref_alt_pattern.match(alt_list[0]):
            raise ParsingError("Invalid format for alternative at line {0}".format(line_nb))
        return alt_list

    def parse_zygosity(self, row, zyg_pos, line_nb):
        try:
            zygosity = row[zyg_pos]
        except Exception:
            raise ParsingError("Unexpected number of fields at line {0}".format(line_nb))
        if zygosity != "Heterozygous" and zygosity != "Homozygous":
            raise ParsingError("Invalid zygosity value: {0} at line {1}".format(zygosity, line_nb))
        else:
            return zygosity


class VCFParser(VariantFormatParser):

    _gt_pattern = re.compile("^(([\.]?[0-9]*([|\/][\.]?[0-9]*)?)|(\.))$")

    def read_maybe_compressed_file(self, input_file, content_type):
        format = content_type.split("/")[1]
        if "x-gzip" == format:
            return gzip.open(input_file, 'rt', encoding='utf-8', errors='replace')
        elif "x-xz" == format:
            return lzma.open(input_file, mode='rt', encoding='utf-8', errors='replace')
        elif "x-bzip2" == format:
            return bz2.open(input_file, mode='rt', encoding='utf-8', errors='replace')
        elif "zip" == format:
            zfile = zipfile.ZipFile(input_file)
            for finfo in zfile.infolist():
                return io.TextIOWrapper(zfile.open(finfo), encoding='utf-8', errors='replace')
        else:
            return io.TextIOWrapper(input_file, encoding='utf-8', errors='replace')

    def parse(self, input_file, content_type="text/plain"):

        vcf_input_stream = self.read_maybe_compressed_file(input_file, content_type)

        header, line_count = self.parse_header(vcf_input_stream)
        self.set_column_indexes(header)
        for line in vcf_input_stream:
            line_count += 1
            line = line.rstrip("\n")
            if line:
                variant = self._create_variant(line, line_count, lambda row: len(row) > 4)
                if variant:
                    yield variant

    def parse_header(self, vcf_input_stream):
        line_count = 0
        for line in vcf_input_stream:
            line_count += 1
            line = line.rstrip("\n")
            if line[0:2] == "##":
                continue
            elif line[0:1] == "#":  # header line
                header_line = line.split("\t")
                return header_line, line_count
            else:
                raise ParsingError("Your submitted VCF does not contain any header.")

    def set_column_indexes(self, header):
        for i in range(len(header)):
            elem = header[i]
            elem = elem.replace('#', '')
            if elem == "CHROM":
                self._chrom_pos = i
            elif elem == "POS":
                self._position_pos = i
            elif elem == "REF":
                self._ref_pos = i
            elif elem == "ALT":
                self._alt_pos = i
            elif elem == "FORMAT":
                self._zyg_pos = i + 1
        # Sanity checks
        if not all(v is not None for v in [self._chrom_pos , self._position_pos , self._ref_pos , self._zyg_pos]):
            raise ParsingError("VCF header must contains fields: "
                               "CHROM, POS, REF, ALT, FORMAT and an extra column for genotype information")
        if self._zyg_pos >= len(header) or self._zyg_pos in (self._chrom_pos, self._position_pos, self._ref_pos, self._alt_pos):
            raise ParsingError("VCF header should contain one column for genotype information (after the FORMAT column)")

    def parse_alt(self, row, alt_pos, line_nb):
        try:
            alt = row[alt_pos]
        except Exception:
            raise ParsingError("Unexpected number of fields at line {0}".format(line_nb))
        # there can be up to three alternative alleles, we keep all options in a list
        alt_list = alt.split(",")
        for alt in alt_list:
            if not self._ref_alt_pattern.match(alt):
                raise ParsingError("Invalid format for alternative at line {0}".format(line_nb))
        return alt_list

    def parse_zygosity(self, row, genotype_info_pos, line_nb):
        sep = ":"
        try:
            format_info = row[genotype_info_pos - 1]
            genotype_info = row[genotype_info_pos]
        except Exception:
            raise ParsingError("Unexpected number of VCF fields at line {0}.".format(line_nb))
        format_info_splitted = format_info.split(sep)
        try:
            gt_idx = format_info_splitted.index("GT")
        except Exception:
            raise ParsingError("Missing GT field in VCF at line {0}: make sure the FORMAT column defines "
                               "correctly the field in the genotype column.".format(line_nb))
        splitted_sample_info = genotype_info.split(sep)
        if gt_idx >= len(splitted_sample_info):
            raise ParsingError("Incorrect VCF genotype format at line {0}: GT from FORMAT column cannot "
                               "be retrieved in the genotype column.".format(line_nb))
        gt = splitted_sample_info[gt_idx]
        if not re.match(self._gt_pattern, gt):
            raise ParsingError("Incorrect zygosity value ('{0}') for field corresponding to genotype (GT) "
                               "at line {1}.".format(gt, line_nb))
        return gt


class GenePanelParser:
    _gene_name_pattern = re.compile("^[A-Za-z-0-9_]+(\@)?$")
    # (taken from https://bioregistry.io/registry/hgnc.symbol)
    _gene_ensg_pattern = re.compile(
        "^((ENSG\d{11}(\.\d+)?)|(FB\w{2}\d{7})|(Y[A-Z]{2}\d{3}[a-zA-Z](\-[A-Z])?)|([A-Z_a-z0-9]+(\.)?(t)?(\d+)?([a-z])?))$")

    # (adapted from https://bioregistry.io/registry/ensembl)

    def validate(self, genes_input, db_credentials):
        """
        Validates the genes for correct identifier and if they are in the DB
        :param genes_input: either a list of lines from manual input or a TextIOWrapper from file input
        :param db_credentials: dictionary containing connection parameters for the database
        :return: list of validated ENSGs (raises error for wrong IDs and if none are left after validation)
        """
        line_count = 0
        gene_panel = {'ensgs': set(), 'names': set()}
        for line in genes_input:
            line_count += 1
            gene = line.strip()
            if gene:
                # order is important here because a gene name also matches the ENSG pattern...
                if re.match(self._gene_name_pattern, gene):
                    gene_panel["names"].add(gene)
                elif re.match(self._gene_ensg_pattern, gene):
                    gene_panel["ensgs"].add(gene)
                else:
                    raise ParsingError("Incorrect gene identifier ('{0}') at line {1}.".format(gene, line_count),
                                       input_type='GENE')
        gene_list = self.check_terms_in_db(gene_panel, db_credentials)
        if len(gene_list) > 0:
            return gene_list
        else:
            raise ParsingError("The gene panel does not contain any valid genes. "
                               "Please review the provided gene names / ENSGs.", input_type='GENE')

    def parse_file(self, gene_panel_file, db_credentials):
        """
        Converts the .txt file with gene names and/or ENSGs, and parses + validates it
        :param gene_panel_file: TemporaryFileWrapper object
        :param db_credentials: dictionary containing connection parameters for the database
        :return: filtered/checked list of ENSGs representing the gene panel
        """
        gene_panel_file = io.TextIOWrapper(gene_panel_file, encoding='utf-8')
        return self.validate(gene_panel_file, db_credentials)

    def parse_manual_input(self, man_input_string, db_credentials):
        """
        Parses the manual input with gene names and/or ENSGs and parses + validates it
        :param man_input_string: manual input (string of genes joined with "\r\n")
        :param db_credentials: dictionary containing connection parameters for the database
        :return: filtered/checked list of ENSGs representing the gene panel
        """
        lines = man_input_string.split("\n")
        return self.validate(lines, db_credentials)

    def check_terms_in_db(self, gene_panel_dict, db_credentials):
        """
        From the genes provided in the gene panel, check if they are in the DB and return the ENSG for all of them.
        :param gene_panel_dict: {'ensgs': set(), 'names': set()}
        :param db_credentials: dictionary containing connection parameters for the database
        :return: list of valid ENSGs for unique genes
        """
        annotator = Annotator(db_credentials)
        annotator.annotation_repository.connect()
        query = '''SELECT ensembl_gene_id, gene_name FROM gene WHERE ensembl_gene_id in ({0}) OR gene_name in ({1})''' \
            .format("'" + "','".join(gene_panel_dict["ensgs"]) + "'", "'" + "','".join(gene_panel_dict["names"]) + "'")
        cur = annotator.annotation_repository.execute(query)
        # some gene names may have multiple ENSGs
        unique_genes_dict = {gene[1]: gene[0] for gene in cur.fetchall()}
        filtered_ensg_list = list(unique_genes_dict.values())
        return filtered_ensg_list


class HPOParser:
    _hpo_pattern = re.compile("^HP:\d{7}$")

    def validate(self, hpo_input, db_credentials):
        """
        Validates the HPO terms for correct ID and if they are in the DB
        :param hpo_input: either a list of lines from manual input or a TextIOWrapper from file input
        :param db_credentials: dictionary containing connection parameters for the database
        :return: list of validated HPO IDs (raises error for wrong IDs and if none are left after validation)
        """
        hpos = set()
        line_count = 0
        for line in hpo_input:
            line_count += 1
            term = line.strip()
            if term:
                if not re.match(self._hpo_pattern, term):
                    raise ParsingError("Incorrect HPO ID ('{0}') at line {1}.".format(term, line_count),
                                       input_type='HPO')
                hpos.add(term)
        hpo_list = self.check_terms_in_db(hpos, db_credentials)
        if len(hpo_list) > 0:
            return hpo_list
        else:
            raise ParsingError("The list of HPO terms does not contain any valid HPO ID. Please review the input.",
                               input_type='HPO')

    def parse_file(self, hpo_file, db_credentials):
        """
        Converts the .txt file and parses + validates it by checking the database
        :param hpo_file: TemporaryFileWrapper object
        :param db_credentials: dictionary containing connection parameters for the database
        :return: validated list of HPO IDs
        """
        hpo_file = io.TextIOWrapper(hpo_file, encoding='utf-8')
        return self.validate(hpo_file, db_credentials)

    def parse_manual_input(self, man_input_string, db_credentials):
        """
        Converts the manual input and parses + validates it
        :param man_input_string: manual input (string of HPOs joined with "\r\n")
        :param db_credentials: dictionary containing connection parameters for the database
        :return: validated list of HPO IDs
        """
        lines = man_input_string.split("\n")
        return self.validate(lines, db_credentials)

    def check_terms_in_db(self, hpos_list, db_credentials):
        """
        From the HPO terms provided, check if they are valid (meaning present in the DB)
        :param hpos_list: list of HPO IDs
        :param db_credentials: dictionary containing connection parameters for the database
        :return: list of valid HPO IDs
        """
        annotator = Annotator(db_credentials)
        annotator.annotation_repository.connect()
        query = '''SELECT hpo_id FROM hpo WHERE hpo_id in ({0})'''.format("'" + "','".join(hpos_list) + "'")
        cur = annotator.annotation_repository.execute(query)
        filtered_list = [row[0] for row in cur.fetchall()]
        return filtered_list


class ParsingError(Exception):
    def __init__(self, message, input_type='VARIANT'):
        super().__init__(message)
        self.input_type = input_type