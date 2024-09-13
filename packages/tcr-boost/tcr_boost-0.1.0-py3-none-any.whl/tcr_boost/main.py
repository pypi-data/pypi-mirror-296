"""
Main module for TCR BOOST.

TCR BOOST: T-Cell Receptor Bayesian Optimization of Specificity and Tuning
"""

import torch
from .data_processing import load_data, preprocess_data
from .surrogate_model import SurrogateModel
from .acquisition import optimize_acquisition
from .sequence_utils import decode_embedding_to_sequence, evaluate_binding_affinity

def run_optimization(num_iterations=5):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    tcr_alpha_sequences, tcr_beta_sequences, binding_affinities = load_data()
    combined_embeddings = preprocess_data(tcr_alpha_sequences, tcr_beta_sequences, device)

    X = torch.tensor(combined_embeddings, dtype=torch.float32).to(device)
    Y = torch.tensor(binding_affinities, dtype=torch.float32).unsqueeze(-1).to(device)

    model = SurrogateModel(X, Y, device)

    for i in range(num_iterations):
        print(f"Iteration {i+1}/{num_iterations}")

        candidate_embedding = optimize_acquisition(model, X, device)

        suggested_alpha_seq, suggested_beta_seq = decode_embedding_to_sequence(
            candidate_embedding, tcr_alpha_sequences, tcr_beta_sequences, combined_embeddings
        )

        new_affinity = evaluate_binding_affinity(suggested_alpha_seq, suggested_beta_seq)
        print("Suggested TCR Alpha Chain Sequence:", suggested_alpha_seq)
        print("Suggested TCR Beta Chain Sequence:", suggested_beta_seq)
        print("Predicted Binding Affinity:", new_affinity)
        print("-" * 50)

        new_embedding = candidate_embedding.unsqueeze(0)
        X = torch.cat([X, new_embedding], dim=0)
        Y = torch.cat([Y, torch.tensor([[new_affinity]], dtype=torch.float32).to(device)], dim=0)

        model.update_model(X, Y)
