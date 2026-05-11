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

# Deep Hash Embedding: no embedding table.
# k hash functions -> dense encoding in [-1,1]^k -> deep MLP -> embedding.
class DHEEmbedding(nn.Module):
    def __init__(self, vocab_sizes, k=64, embedding_dim=32,
                 hidden_layers=3, dnn_width=128):
        super().__init__()
        self.k = k
        self.embedding_dim = embedding_dim
        self.num_fields = len(vocab_sizes)
        m = 10**6

        torch.manual_seed(0)
        self.register_buffer('hash_a',
            torch.randint(1, 2**31 - 1, (k,), dtype=torch.long))
        self.register_buffer('hash_b',
            torch.randint(0, 2**31 - 1, (k,), dtype=torch.long))
        self.register_buffer('hash_p',
            torch.tensor(m + 7, dtype=torch.long))
        self.m = m

        # DNN: BatchNorm1d safe here — input always (N, k) flat
        layers = [nn.Linear(k, dnn_width), nn.BatchNorm1d(dnn_width), nn.Mish()]
        for _ in range(hidden_layers - 1):
            layers += [nn.Linear(dnn_width, dnn_width),
                       nn.BatchNorm1d(dnn_width), nn.Mish()]
        layers.append(nn.Linear(dnn_width, embedding_dim))
        self.dnn = nn.Sequential(*layers)

        # Init DNN weights
        for m_layer in self.dnn:
            if isinstance(m_layer, nn.Linear):
                nn.init.xavier_uniform_(m_layer.weight)
                if m_layer.bias is not None:
                    nn.init.zeros_(m_layer.bias)

    def _encode(self, ids):
        ids = ids.unsqueeze(1).long()             # (N, 1)
        h = ((self.hash_a * ids + self.hash_b)
             % self.hash_p) % self.m              # (N, k)
        return h.float() / (self.m - 1) * 2 - 1  # (N, k) in [-1, 1]

    def forward(self, x):
        B = x.size(0)
        enc = self._encode(x.reshape(-1))         # (B*F, k)
        emb = self.dnn(enc)                        # (B*F, embedding_dim)
        return emb.view(B, self.num_fields, self.embedding_dim)