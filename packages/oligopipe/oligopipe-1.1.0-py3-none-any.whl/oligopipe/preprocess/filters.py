import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Filter(Enum):
    MAX_MAF = "MAF &le;"
    REMOVE_INTERGENIC = "Remove Intergenic"
    REMOVE_INTRONS = "Remove intronic/synonymous"
    REMOVE_INTRONS_AND_SYNONYMOUS = "Remove intronic and all synonymous"

    @staticmethod
    def get_variant_filter_types(filters):
        return list(map(lambda r: Filter.get_variant_filter_type(r), filters))

    @staticmethod
    def get_variant_filter_type(filter):
        if isinstance(filter, tuple):
            return Filter[filter[0]]
        else:
            return Filter[filter]

    @staticmethod
    def get_variant_filter_value(filters, filter_type):
        for filtr in filters:
            if Filter.get_variant_filter_type(filtr) == filter_type:
                return filtr[1]
