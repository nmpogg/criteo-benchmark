import torch
import torch.nn as nn
import torch.nn.functional as F

class PureHashEmbedding(nn.Module):
    def __init__(self, hash_buckets, embedding_dim=64):
        """
        hash_buckets: Kích thước bảng băm. 
        Để công bằng về bộ nhớ với mô hình của bạn, ta set hash_buckets = 250,000.
        (250k * 64 tốn RAM xấp xỉ với phương pháp Hybrid của bạn).
        """
        super(PureHashEmbedding, self).__init__()
        self.hash_buckets = hash_buckets
        # Chỉ lưu 1 bảng nhỏ gọn
        self.emb = nn.Embedding(hash_buckets, embedding_dim)

    def forward(self, x, frequency_groups=None):
        # Băm toàn bộ ID (kể cả Head hay Tail)
        hashed_ids = x % self.hash_buckets
        return self.emb(hashed_ids)