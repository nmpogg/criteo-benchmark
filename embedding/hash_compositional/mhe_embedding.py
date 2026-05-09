"""
Multiple Hash Embeddings (MHE)
2021

Sử dụng K bảng embedding nhỏ song song. Mỗi bảng có B buckets (B << vocab_size).
Mỗi item được map vào một bucket trong mỗi bảng bằng hàm hash khác nhau,
kết quả K embeddings được cộng lại (element-wise sum).

Ưu điểm:
- Memory: O(K × B × d) vs O(V × d) — giảm đáng kể khi V >> B
- Nhiều hash functions → giảm collision hiệu quả
- Không cần MLP phụ như DHE → forward pass nhanh hơn

Cách dùng:
    from mhe_embedding import MHEEmbedding, MHEEmbeddingLayer, IntegerMLP
"""

import math
import numpy as np
import torch
import torch.nn as nn


# ---------------------------------------------------------------------------
# MHEEmbedding 
# ---------------------------------------------------------------------------

class MHEEmbedding(nn.Module):
    """
    Multiple Hash Embeddings cho một categorical feature.

    f(id) = sum_{k=1}^{K} E_k[ h_k(id) ]

    Mỗi hàm hash: h_k(x) = (a_k * x + b_k) mod B
    Các hệ số a_k lẻ để coprime với B chẵn → phân phối bucket đều hơn.

    Args:
        vocab_size  : số lượng unique values
        embed_dim   : chiều embedding output
        num_hashes  : K — số bảng hash
        bucket_size : target số buckets B (sẽ bị giới hạn bởi vocab_size)
        seed        : random seed
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 64,
        num_hashes: int = 4,
        bucket_size: int = 2000,
        seed: int = 42,
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.embed_dim  = embed_dim
        self.num_hashes = num_hashes

        # Fix: B không được lớn hơn vocab_size (tránh lãng phí với vocab nhỏ)
        self.B = min(vocab_size, bucket_size)

        # K embedding tables, mỗi table shape (B, embed_dim)
        self.tables = nn.ModuleList([
            nn.Embedding(self.B, embed_dim)
            for _ in range(num_hashes)
        ])

        # Khởi tạo với scale nhỏ để tổng K tables không bị quá lớn
        std = 1.0 / math.sqrt(embed_dim * num_hashes)
        for emb in self.tables:
            nn.init.normal_(emb.weight, mean=0.0, std=std)

        # Hash params cố định
        rng = np.random.RandomState(seed)
        # a_k lẻ → đảm bảo coprime với B chẵn
        a_vals = rng.choice(
            range(1, self.B * 2 + 1, 2),   # chỉ lấy số lẻ
            size=num_hashes,
            replace=num_hashes > self.B,
        )
        b_vals = rng.randint(0, self.B, size=num_hashes)
        self.register_buffer('hash_a', torch.tensor(a_vals, dtype=torch.long))
        self.register_buffer('hash_b', torch.tensor(b_vals, dtype=torch.long))

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        """
        ids : (batch,) LongTensor
        returns : (batch, embed_dim) FloatTensor — sum of K embeddings
        """
        result = None
        for k in range(self.num_hashes):
            bucket = (ids * self.hash_a[k] + self.hash_b[k]) % self.B
            emb_k  = self.tables[k](bucket)   # (batch, embed_dim)
            result = emb_k if result is None else result + emb_k
        return result   # (batch, embed_dim)

    def memory_stats(self) -> dict:
        mhe_params   = self.num_hashes * self.B * self.embed_dim
        naive_params = self.vocab_size * self.embed_dim
        return {
            'vocab_size'   : self.vocab_size,
            'B'            : self.B,
            'K'            : self.num_hashes,
            'mhe_params'   : mhe_params,
            'naive_params' : naive_params,
            'ratio'        : mhe_params / max(naive_params, 1),
        }

    def extra_repr(self) -> str:
        return (f'vocab_size={self.vocab_size}, B={self.B}, '
                f'K={self.num_hashes}, embed_dim={self.embed_dim}')


