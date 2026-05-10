"""
Deep Hash Embedding (DHE)
Google KDD 2021

Thay thế embedding lookup table bằng một mạng MLP nhỏ nhận đầu vào
là k hash values của item ID, giúp giảm bộ nhớ mà vẫn học được
biểu diễn phong phú thông qua quá trình training.

"""

import math
import numpy as np
import torch
import torch.nn as nn


# ---------------------------------------------------------------------------
# DHEEmbedding 
# ---------------------------------------------------------------------------

class DHEEmbedding(nn.Module):
    """
    Deep Hash Embedding cho một categorical feature.

    Với mỗi item id:
      1. Tính k hash values bằng k hàm hash tuyến tính khác nhau
         h_i(x) = (a_i * x + b_i) mod vocab_size
      2. Normalize về [-1, 1]
      3. Đưa qua MLP: k → hidden_dims → embed_dim

    Args:
        vocab_size  : số lượng unique values của feature này
        embed_dim   : chiều output embedding (thường 64)
        num_hashes  : số hàm hash k (thường 512–1024)
        hidden_dims : list các hidden layer sizes của MLP
        seed        : random seed để tái lập kết quả
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 64,
        num_hashes: int = 1024,
        hidden_dims: list = None,
        seed: int = 42,
    ):
        super().__init__()
        if hidden_dims is None:
            hidden_dims = [512, 256]

        self.vocab_size = vocab_size
        self.embed_dim  = embed_dim
        self.num_hashes = num_hashes

        # --- Hash params cố định (không train) ---
        # Dùng universal hashing: h(x) = (ax + b) mod p mod vocab_size
        large_prime = 2_147_483_647  # 2^31 - 1 (Mersenne prime)
        rng = np.random.RandomState(seed)
        self.register_buffer(
            'hash_a',
            torch.tensor(rng.randint(1, large_prime, size=(num_hashes,)), dtype=torch.long)
        )
        self.register_buffer(
            'hash_b',
            torch.tensor(rng.randint(0, large_prime, size=(num_hashes,)), dtype=torch.long)
        )

        # --- DHE MLP ---
        layers = []
        in_dim = num_hashes
        for h_dim in hidden_dims:
            layers += [
                nn.Linear(in_dim, h_dim),
                nn.LayerNorm(h_dim),
                nn.ReLU(),
            ]
            in_dim = h_dim
        layers.append(nn.Linear(in_dim, embed_dim))
        self.mlp = nn.Sequential(*layers)

        self._init_weights()

    def _init_weights(self):
        for module in self.mlp.modules():
            if isinstance(module, nn.Linear):
                nn.init.kaiming_normal_(module.weight, nonlinearity='relu')
                if module.bias is not None:
                    nn.init.zeros_(module.bias)

    def _hash_encode(self, ids: torch.Tensor) -> torch.Tensor:
        """
        ids : (batch,) LongTensor
        returns : (batch, num_hashes) FloatTensor trong [-1, 1]
        """
        # (batch, 1) broadcast với (1, num_hashes)
        ids_col = ids.unsqueeze(1)                                    # (batch, 1)
        hashed  = (ids_col * self.hash_a + self.hash_b) % self.vocab_size  # (batch, k)
        # Normalize về [-1, 1]
        encoded = hashed.float() / max(self.vocab_size - 1, 1) * 2 - 1
        return encoded

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        """
        ids : (batch,) LongTensor — encoded category indices
        returns : (batch, embed_dim) FloatTensor
        """
        encoded = self._hash_encode(ids)   # (batch, num_hashes)
        return self.mlp(encoded)           # (batch, embed_dim)

    def extra_repr(self) -> str:
        return (f'vocab_size={self.vocab_size}, embed_dim={self.embed_dim}, '
                f'num_hashes={self.num_hashes}')


