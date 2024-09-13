"""
Sequence utilities module for TCR BOOST.

TCR BOOST: T-Cell Receptor Bayesian Optimization of Specificity and Tuning
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors

def decode_embedding_to_sequence(embedding, alpha_sequences, beta_sequences, combined_embeddings):
    nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(combined_embeddings)
    embedding_np = embedding.cpu().detach().numpy().reshape(1, -1)
    _, indices = nbrs.kneighbors(embedding_np)
    idx = indices[0][0]
    alpha_seq = alpha_sequences[idx]
    beta_seq = beta_sequences[idx]
    return alpha_seq, beta_seq

def evaluate_binding_affinity(alpha_seq, beta_seq):
    # Placeholder for actual binding affinity evaluation
    # Replace this with your evaluation method
    return np.random.rand()
