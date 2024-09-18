import importlib.resources

from scipy.sparse import spdiags
import numpy as np
from numpy.linalg import norm
import pickle


def iterate(A, q, c=0.15, epsilon=1e-9,
            max_iters=100, norm_type=1):
    """
    Perform power iteration for RWR, PPR, or PageRank

    inputs
        A : csr_matrix
            input matrix (for RWR and it variants, it should be row-normalized)
        q : ndarray
            query vector
        c : float
            restart probability
        epsilon : float
            error tolerance for power iteration
        max_iters : int
            maximum number of iterations for power iteration
        handles_deadend : bool
            if true, it will handle the deadend issue in power iteration
            otherwise, it won't, i.e., no guarantee for sum of RWR scores
            to be 1 in directed graphs
        norm_type : int
            type of norm used in measuring residual at each iteration
    outputs
        x : ndarray
            result vector
    """
    x = q
    old_x = q
    residuals = np.zeros(max_iters)

    for i in range(max_iters):
        x = (1 - c) * (A.dot(old_x)) + (c * q)

        residuals[i] = norm(x - old_x, norm_type)

        if residuals[i] <= epsilon:
            break

        old_x = x

    return x, residuals[0:i + 1]


class RWR:
    normalized = False

    def __init__(self, A):
        self.A = A
        self.m, self.n = self.A.shape
        self.node_ids = np.arange(0, self.n)
        self.normalize()

    def normalize(self):
        '''
        Perform row-normalization of the adjacency matrix
        '''
        if self.normalized is False:
            nA = self.row_normalize(self.A)
            self.nAT = nA.T
            self.normalized = True

    def row_normalize(self, A):
        '''
        Perform row-normalization of the given matrix

        inputs
            A : csr_matrix
                (n x n) input matrix where n is # of nodes
        outputs
            nA : crs_matrix
                 (n x n) row-normalized matrix
        '''
        n = A.shape[0]

        # do row-wise sum where d is out-degree for each node
        d = A.sum(axis=1)
        d = np.asarray(d).flatten()

        # handle 0 entries in d
        d = np.maximum(d, np.ones(n))
        invd = 1.0 / d

        invD = spdiags(invd, 0, n, n)

        # compute row normalized adjacency matrix by nA = invD * A
        nA = invD.dot(A)

        return nA

    def compute(self, seed_vector, c, epsilon, max_iters):
        '''
        Compute the RWR score vector w.r.t. the seed node

        inputs
            seed : int
                seed (query) node id
            c : float
                restart probability
            epsilon : float
                error tolerance for power iteration
            max_iters : int
                maximum number of iterations for power iteration
            handles_deadend : bool
                if true, it will handle the deadend issue in power iteration
                otherwise, it won't, i.e., no guarantee for sum of RWR scores
                to be 1 in directed graphs
        outputs
            r : ndarray
                RWR score vector
        '''
        self.normalize()
        q = seed_vector
        r, residuals = iterate(self.nAT, q, c, epsilon, max_iters)

        return r

    def check_seeds(self, seeds):
        for seed in seeds:
            if seed < 0 or seed >= self.n:
                raise ValueError('Out of range of seed node id')


def run_rwr_hop(annotated_variants, seeds_list):
    with importlib.resources.open_binary('oligopipe.hop', 'final_wholeKG_matrix.p') as file:
        matrix = pickle.load(file)
    with importlib.resources.open_binary('oligopipe.hop', 'final_instances_to_index.p') as file:
        instances_to_index = pickle.load(file)
    with importlib.resources.open_binary('oligopipe.hop', 'all_genes.p') as file:
        all_genes = pickle.load(file)
    seed_vector = np.zeros(len(instances_to_index.keys()))
    seed_names = [s for s in seeds_list if s in instances_to_index]
    for s in seed_names:
        seed_vector[instances_to_index[s]] = 1 / len(seed_names)
    rwr = RWR(matrix)
    results = rwr.compute(seed_vector, c=0.3, epsilon=1e-9, max_iters=100)
    # Put results in dict format
    list_instances_to_index_keys = list(instances_to_index.keys())
    results = {list_instances_to_index_keys[i]: results[i] for i in range(len(instances_to_index.keys())) if
               all_genes.get(list_instances_to_index_keys[i]) is not None}

    # Normalize results for genes
    max_rwr = max(results.values())
    min_rwr = min(results.values())
    normalized_results = {g: (r - min_rwr) / (max_rwr - min_rwr) for g, r in results.items()}

    # Obtain min max for patient gene pairs
    patient_genes = list(set([g.gene.ensembl_gene for g in annotated_variants]))
    sorted_rwr_scores = sorted([normalized_results.get(g,0) for g in patient_genes])
    max_pair = (sorted_rwr_scores[-1] + sorted_rwr_scores[-2])/2
    min_pair = (sorted_rwr_scores[0] + sorted_rwr_scores[1])/2
    return normalized_results, max_pair, min_pair