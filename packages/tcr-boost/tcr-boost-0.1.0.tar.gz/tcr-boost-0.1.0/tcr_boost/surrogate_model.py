"""
Surrogate model module for TCR BOOST.

TCR BOOST: T-Cell Receptor Bayesian Optimization of Specificity and Tuning
"""

import torch
from gpytorch.models import ExactGP
from gpytorch.kernels import ScaleKernel, RBFKernel
from gpytorch.means import ZeroMean
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.mlls import ExactMarginalLogLikelihood

class GPRegressionModel(ExactGP):
    def __init__(self, train_x, train_y, likelihood):
        super(GPRegressionModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ZeroMean()
        self.covar_module = ScaleKernel(RBFKernel())

    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return torch.distributions.MultivariateNormal(mean_x, covar_x)

class SurrogateModel:
    def __init__(self, X, Y, device):
        self.device = device
        self.likelihood = GaussianLikelihood().to(self.device)
        self.model = GPRegressionModel(X, Y.squeeze(), self.likelihood).to(self.device)
        self.mll = ExactMarginalLogLikelihood(self.likelihood, self.model)
        self.fit_model()

    def fit_model(self):
        self.model.train()
        self.likelihood.train()

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.1)
        training_iterations = 50

        for _ in range(training_iterations):
            optimizer.zero_grad()
            output = self.model(self.model.train_inputs[0])
            loss = -self.mll(output, self.model.train_targets)
            loss.backward()
            optimizer.step()

    def predict(self, X):
        self.model.eval()
        self.likelihood.eval()
        with torch.no_grad(), torch.cuda.amp.autocast():
            pred_dist = self.likelihood(self.model(X))
        return pred_dist

    def update_model(self, X_new, Y_new):
        self.model.set_train_data(inputs=X_new, targets=Y_new.squeeze(), strict=False)
        self.fit_model()
