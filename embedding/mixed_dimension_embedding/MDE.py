import torch
import torch.nn as nn
import math

class MixedDimensionEmbedding(nn.Module):
    """
    Mixed Dimension Embeddings (MDE)
    Based on the paper: "Mixed Dimension Embeddings with Application to Memory-Efficient Recommendation Systems" (Ginart et al., 2019)
    https://arxiv.org/pdf/1909.11810
    
    This module divides the vocabulary into K blocks based on frequency.
    Each block has its own embedding dimension to save memory. A linear projection matrix
    lifts the lower-dimensional embeddings to a uniform base dimension.
    """
    def __init__(self, block_vocab_sizes, base_dim, block_embedding_dims=None, alpha=None, block_frequencies=None):
        """
        Args:
            block_vocab_sizes (list of int): The number of unique items (vocabulary size) in each block.
            base_dim (int): The uniform base dimension to which all embeddings will be projected.
            block_embedding_dims (list of int, optional): Explicit embedding dimensions for each block.
            alpha (float, optional): The alpha parameter for the alpha-power rule (d_i \propto f_i^\alpha).
            block_frequencies (list of float, optional): The average/representative frequency for each block.
                                                         Required if alpha is provided to auto-calculate dimensions.
        """
        super(MixedDimensionEmbedding, self).__init__()
        
        self.num_blocks = len(block_vocab_sizes)
        self.base_dim = base_dim
        
        # 1. Tự động tính toán số chiều nếu có truyền alpha và tần suất
        if alpha is not None and block_frequencies is not None:
            if len(block_frequencies) != self.num_blocks:
                raise ValueError("block_frequencies must have the same length as block_vocab_sizes.")
            
            # Lấy tần suất cao nhất làm chuẩn (thường là block 0 - head)
            f_max = float(max(block_frequencies))
            
            block_embedding_dims = []
            for f in block_frequencies:
                # Alpha-power rule: d_i = base_dim * (f_i / f_max)^alpha
                raw_dim = base_dim * ((float(f) / f_max) ** alpha)
                
                # Làm tròn thành lũy thừa của 2 (Power of 2)
                dim = max(1, 2 ** round(math.log2(max(raw_dim, 1e-9))))
                dim = min(dim, base_dim)  # Đảm bảo không vượt quá base_dim
                block_embedding_dims.append(int(dim))
                
        elif block_embedding_dims is None:
            raise ValueError("Bạn phải cung cấp block_embedding_dims hoặc (alpha VÀ block_frequencies).")
            
        if len(block_vocab_sizes) != len(block_embedding_dims):
            raise ValueError("block_vocab_sizes and block_embedding_dims must have the same length.")
            
        self.block_embedding_dims = block_embedding_dims
        
        # 2. Khởi tạo danh sách các Embedding tables và Projections
        self.embeddings = nn.ModuleList()
        self.projections = nn.ModuleList()
        
        for vocab_size, emb_dim in zip(block_vocab_sizes, self.block_embedding_dims):
            self.embeddings.append(nn.Embedding(vocab_size, emb_dim))
            
            # Projection matrix (V = E P), không dùng bias để tiết kiệm tham số theo paper
            if emb_dim != base_dim:
                self.projections.append(nn.Linear(emb_dim, base_dim, bias=False))
            else:
                self.projections.append(nn.Identity())
                
    def forward(self, x, block_indices):
        """
        Args:
            x (torch.Tensor): Tensor of item IDs. IDs must be locally indexed within their blocks (0 to block_vocab_size-1).
            block_indices (torch.Tensor): Tensor indicating which block each item belongs to (0 to num_blocks - 1).
            
        Returns:
            torch.Tensor: The projected embeddings of shape (*x.shape, base_dim).
        """
        # Khởi tạo output tensor có cùng device với input
        out = torch.zeros(*x.shape, self.base_dim, device=x.device, dtype=self.embeddings[0].weight.dtype)
        
        for i in range(self.num_blocks):
            mask = (block_indices == i)
            
            if mask.any():
                local_ids = x[mask]
                embs = self.embeddings[i](local_ids)
                projected_embs = self.projections[i](embs)
                out[mask] = projected_embs
                
        return out


# Gọi tự động bằng luật alpha-power
mde = MixedDimensionEmbedding(
    block_vocab_sizes=[1000, 5000, 20000],
    base_dim=64,
    alpha=0.5,
    block_frequencies=[10000.0, 100.0, 1.0] # Tần suất trung bình hoặc tổng truy cập của từng block
)

print(mde.block_embedding_dims) 
# Đầu ra sẽ tự động làm tròn về lũy thừa của 2, ví dụ: [64, 8, 1] tùy vào alpha
