import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
import time
from collections import defaultdict
warnings.filterwarnings('ignore')

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from torch.nn import functional as F

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import roc_auc_score, roc_curve, log_loss
from sklearn.model_selection import train_test_split


class AutoEmbEmbedding(nn.Module):
    def __init__(self, vocab_sizes, candidate_dims=None, max_dim=32,
                 controller_hidden=64):
        super().__init__()
        if candidate_dims is None:
            candidate_dims = [2, 16, 32]
        self.candidate_dims = candidate_dims
        self.max_dim = max_dim
        self.embedding_dim = max_dim
        self.num_fields = len(vocab_sizes)
        N = len(candidate_dims)

        self.embeddings = nn.ModuleList([
            nn.ModuleList([nn.Embedding(v, d) for d in candidate_dims])
            for v in vocab_sizes
        ])
        for field_embs in self.embeddings:
            for emb in field_embs:
                nn.init.normal_(emb.weight, 0, 0.01)

        self.proj = nn.ModuleList([
            nn.Linear(d, max_dim, bias=True) for d in candidate_dims
        ])
        for lin in self.proj:
            nn.init.xavier_uniform_(lin.weight)
            nn.init.zeros_(lin.bias)

        self.ln = nn.LayerNorm(max_dim)

        # Controller: 1 -> hidden -> N weights
        self.controller = nn.Sequential(
            nn.Linear(1, controller_hidden), nn.ReLU(),
            nn.Linear(controller_hidden, N), nn.Softmax(dim=-1)
        )

    def forward(self, x):
        embed_out = []
        for m in range(self.num_fields):
            ids = torch.clamp(x[:, m], 0,
                              self.embeddings[m][0].num_embeddings - 1)
            pop = torch.log1p(ids.float()).unsqueeze(1)  # (B, 1)
            weights = self.controller(pop)               # (B, N)

            field_emb = torch.zeros(
                x.size(0), self.max_dim, device=x.device)
            for n in range(len(self.candidate_dims)):
                e = self.embeddings[m][n](ids)
                e = self.proj[n](e)
                e = torch.tanh(self.ln(e))
                field_emb = field_emb + weights[:, n:n+1] * e

            embed_out.append(field_emb)

        return torch.stack(embed_out, dim=1)  # (B, F, max_dim)