"""
Acquisition function module for TCR BOOST.

TCR BOOST: T-Cell Receptor Bayesian Optimization of Specificity and Tuning
"""

import torch
from botorch.acquisition import UpperConfidenceBound
from botorch.optim import optimize_acqf

def optimize_acquisition(model, X, device):
    acq_func = UpperConfidenceBound(model.model, beta=2.0)
    bounds = torch.stack([X.min(dim=0).values, X.max(dim=0).values]).to(device)

    candidate, _ = optimize_acqf(
        acq_function=acq_func,
        bounds=bounds,
        q=1,
        num_restarts=5,
        raw_samples=20,
    )

    return candidate.squeeze(0)
