import torch
import torch.nn as nn
import math

class MixedDimensionEmbedding(nn.Module):
    def __init__(self, block_vocab_sizes, base_dim, alpha=0.5):
        super(MixedDimensionEmbedding, self).__init__()
        self.num_blocks = len(block_vocab_sizes)
        self.base_dim = base_dim
        
        self.embeddings = nn.ModuleList()
        self.projections = nn.ModuleList()
        
        # Tìm vocab_size nhỏ nhất (tương ứng với xác suất truy vấn cao nhất)
        v_min = float(min(block_vocab_sizes))
        
        for vocab_size in block_vocab_sizes:
            # 1. Tính số chiều tỷ lệ NGHỊCH với vocab_size (chuẩn theo paper Facebook)
            raw_dim = base_dim * ((v_min / float(vocab_size)) ** alpha)
            
            # Làm tròn về lũy thừa của 2 gần nhất (1, 2, 4, 8, 16, 32, 64)
            dim = max(1, 2 ** round(math.log2(max(raw_dim, 1e-9))))
            dim = min(dim, base_dim)
            emb_dim = int(dim)
            
            print(f"Vocab: {vocab_size} -> Dim: {emb_dim}")
            
            # 2. Khởi tạo Embedding
            self.embeddings.append(nn.Embedding(vocab_size, emb_dim))
            
            # 3. Khởi tạo Linear Projection để đưa về base_dim
            if emb_dim != base_dim:
                self.projections.append(nn.Linear(emb_dim, base_dim, bias=False))
            else:
                self.projections.append(nn.Identity())
                
    def forward(self, cat_x):
        # cat_x có shape: (batch_size, num_blocks)
        projected_embs = []
        
        # Lặp qua từng cột (từng feature)
        for i in range(self.num_blocks):
            # Lấy toàn bộ batch của feature thứ i
            feature_col = cat_x[:, i] 
            
            # Đi qua Embedding -> (batch_size, emb_dim)
            emb = self.embeddings[i](feature_col)
            
            # Đi qua Projection -> (batch_size, base_dim)
            proj = self.projections[i](emb)
            
            projected_embs.append(proj)
            
        # Ghép nối tất cả dọc theo chiều feature -> (batch_size, num_blocks * base_dim)
        return torch.cat(projected_embs, dim=1)


# Gọi tự động bằng luật alpha-power
mde = MixedDimensionEmbedding(
    block_vocab_sizes=[1000, 5000, 20000],
    base_dim=64,
    alpha=0.5
)

