"""
Data processing module for TCR BOOST.

TCR BOOST: T-Cell Receptor Bayesian Optimization of Specificity and Tuning
"""

import numpy as np
import torch
import esm

def load_data():
    # Placeholder for actual data loading
    # Replace this with code to load your dataset
    num_sequences = 100
    sequence_length_alpha = 15
    sequence_length_beta = 15

    amino_acids = list('ACDEFGHIKLMNPQRSTVWY')

    def generate_dummy_sequences(num_sequences, sequence_length):
        sequences = [''.join(np.random.choice(amino_acids, sequence_length)) for _ in range(num_sequences)]
        return sequences

    tcr_alpha_sequences = generate_dummy_sequences(num_sequences, sequence_length_alpha)
    tcr_beta_sequences = generate_dummy_sequences(num_sequences, sequence_length_beta)
    binding_affinities = np.random.rand(num_sequences)

    return tcr_alpha_sequences, tcr_beta_sequences, binding_affinities

def preprocess_data(tcr_alpha_sequences, tcr_beta_sequences, device):
    # Load the ESM-1b model
    model, alphabet = esm.pretrained.esm1b_t33_650M_UR50S()
    batch_converter = alphabet.get_batch_converter()
    model = model.to(device)
    model.eval()

    def encode_sequences(sequences):
        data = [("sequence", seq) for seq in sequences]
        batch_labels, batch_strs, batch_tokens = batch_converter(data)
        batch_tokens = batch_tokens.to(device)

        with torch.no_grad():
            results = model(batch_tokens, repr_layers=[33], return_contacts=False)
        token_representations = results["representations"][33]

        sequence_embeddings = []
        for i, (_, seq) in enumerate(data):
            embedding = token_representations[i, 1:len(seq)+1].mean(0)
            sequence_embeddings.append(embedding.cpu().numpy())
        return np.vstack(sequence_embeddings)

    # Encode alpha and beta sequences
    alpha_embeddings = encode_sequences(tcr_alpha_sequences)
    beta_embeddings = encode_sequences(tcr_beta_sequences)
    combined_embeddings = np.hstack((alpha_embeddings, beta_embeddings))

    return combined_embeddings
