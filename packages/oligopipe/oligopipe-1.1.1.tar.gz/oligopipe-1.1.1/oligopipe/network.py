import logging

import networkx as nx

logger = logging.getLogger(__name__)


class OligoNetwork(nx.Graph):
    """
    Oligogenic network based on result of VarCoPP.
    It connects genes that have at least one variant combination predicted as pathogenic,
    and edges are weighted with the highest VarCoPP score for that pair.

    Format of a triangle graph A,B,C with scores: (A,B)=(2, 3, 5) (scores from multiple variant combs) ;
    (B,C)=3 ; (A,C)=6 ; will give: {"A":{"B":5, "C":6},"B":{"A":5, "C":3}, "C":{"A":6,"B":3}}
    """

    def __init__(self, data):
        """
        Create the gene network
        :param data: result JSON from VarCoPP execution
        """
        super().__init__()
        graph = {}
        nodes = []
        links = []
        dict_links = {}
        if "combinations" in data:
            for comb_id, comb in data["combinations"].items():
                ens_gene_A = comb['varA']['ensembl_gene']
                ens_gene_B = comb['varB']['ensembl_gene']

                geneA = ens_gene_A + ':' + data["genes"][ens_gene_A]["gene_name"]
                geneB = ens_gene_B + ':' + data["genes"][ens_gene_B]["gene_name"]

                # only disease-causing
                if comb['prediction'] != 'Neutral':

                    if geneA not in nodes:
                        nodes.append(geneA)
                        graph[geneA] = {'links': {}, 'centrality': {}}
                    if geneB not in nodes:
                        nodes.append(geneB)
                        graph[geneB] = {'links': {}, 'centrality': {}}

                    if (geneA, geneB) not in links:
                        links.append((geneA, geneB))
                        dict_links[(geneA, geneB)] = {'max_score': comb['varcopp_score']}
                        graph[geneA]['links'][geneB] = comb['varcopp_score']
                        graph[geneB]['links'][geneA] = comb['varcopp_score']

                    elif comb['varcopp_score'] > dict_links[(geneA, geneB)]['max_score']:
                        dict_links[(geneA, geneB)]['max_score'] = comb['varcopp_score']
                        graph[geneA]['links'][geneB] = comb['varcopp_score']
                        graph[geneB]['links'][geneA] = comb['varcopp_score']

        self._graph = graph
        self.add_nodes_from(nodes)
        self.add_edges_from(links)
        nx.set_edge_attributes(self, dict_links)

    def set_closeness(self):
        """
        Adds the closeness of the nodes (genes) to the graph dict
        """
        bb = nx.closeness_centrality(self)
        nx.set_node_attributes(self, bb, 'closeness')

        for node in bb:
            self._graph[node]['centrality']['closeness'] = bb[node]

    def set_degree(self):
        """
        Adds the degree of the nodes (genes) to the graph dict
        """
        degrees = self.degree()
        for node, degree in degrees:
            self._graph[node]['centrality']['degree'] = degree

    def get_graph(self):
        """
        Returns the graph dict
        :return: dict as {source_node: {"links": {target_node: score}, "centrality": {}}}
        """
        return self._graph

    def get_augmented_graph(self):
        """
        Returns the OligoNetwork graph dict, augmented with closeness and degree centrality measures
        :return: dict as {"source_node": {"links": {target_node: score}, "centrality": {"closeness": , "degree": }}}
        """
        self.set_closeness()
        self.set_degree()
        return self.get_graph()

    @staticmethod
    def filter(graph_dict, edge_min=None, edge_max=None, filtered_nodes=None,
               filtered_nodes_include_mode=False, **kwargs):
        """
        Filter a graph based on edge weights (VarCoPP score) or a set of nodes to include/exclude
        :param graph_dict: dict from get_augmented_graph()
                Note: we use this because the filtering is done on the frontend -> better to work with the dictionary
        :param edge_min: minimum edge weight
        :param edge_max: maximum edge weight
        :param filtered_nodes: list of node IDs (genes)
        :param filtered_nodes_include_mode: boolean; whether the "filtered_nodes" should be included (default: excluded)
        :return: filtered graph dict
        """
        filtered_nodes_include_mode = bool(filtered_nodes_include_mode)
        if ":" not in list(graph_dict.keys())[0]:
            filtered_nodes = [n.split(":")[1] for n in filtered_nodes]
        filtered_graph = {}
        for node, value in graph_dict.items():
            node_name = node.split(":")[1] if ":" in node else node
            if (not filtered_nodes_include_mode) ^ (node_name in filtered_nodes):
                filtered_graph[node] = {k: v for k, v in graph_dict[node].items() if k != "links"}
                filtered_graph[node]["links"] = {}
                for link, score in value["links"].items():
                    link_name = link.split(":")[1] if ":" in link else link
                    if (not filtered_nodes_include_mode) ^ (link_name in filtered_nodes):
                        if not edge_min or score >= float(edge_min):
                            if not edge_max or score <= float(edge_max):
                                filtered_graph[node]["links"][link] = score
        return filtered_graph

    @staticmethod
    def export_to_graphml(graph_dict):
        """
        Generates GraphML
        :param graph_dict: dict from get_graph() or get_augmented_graph()
        :return: String representing the GraphML
        """
        G = nx.Graph()
        for node, value in graph_dict.items():
            node_id = None
            meta = {}
            if ":" in node:
                node_id, node = node.split(":")
            if node_id:
                meta["id"] = node_id
            if "meta" in value:
                for k, v in value["meta"].items():
                    if v is not None:
                        meta[k] = v
            if "selected" in value:
                meta["oligogenic_module"] = value["selected"]
            G.add_node(node, **meta)
            if "links" in value:
                for link, score in value["links"].items():
                    if ":" in link:
                        link_id, link = link.split(":")
                    G.add_edge(node, link, weight=score)
        return '\n'.join(nx.generate_graphml(G))


if __name__ == "__main__":
    net = OligoNetwork()
    net.set_closeness()
    net.set_degree()
    print(net.edges(data=True))
    print(net.nodes(data=True))
    print(net.get_graph())