import torch
import torch.nn as nn
import torch.nn.functional as F

class MixedDimLinearEmbedding(nn.Module):
    def __init__(self, num_head, num_mid, num_tail, 
                 dim_head=64, dim_mid=32, dim_tail=16, unified_dim=64):
        super(MixedDimLinearEmbedding, self).__init__()
        self.unified_dim = unified_dim
        
        # 1. Khởi tạo 3 bảng kích thước khác nhau
        self.head_emb = nn.Embedding(num_head, dim_head)
        self.mid_emb = nn.Embedding(num_mid, dim_mid)
        self.tail_emb = nn.Embedding(num_tail, dim_tail)
        
        # 2. Projection Layers (Thủ phạm gây tốn FLOPs và làm chậm mô hình)
        # Bảng Head đã là 64 chiều nên không cần Linear
        self.proj_mid = nn.Linear(dim_mid, unified_dim)
        self.proj_tail = nn.Linear(dim_tail, unified_dim)

    def forward(self, x, frequency_groups):
        batch_size = x.size(0)
        out = torch.zeros(batch_size, self.unified_dim, device=x.device)
        
        mask_head = (frequency_groups == 0)
        mask_mid = (frequency_groups == 1)
        mask_tail = (frequency_groups == 2)
        
        # Nhóm Head: Lấy trực tiếp
        if mask_head.any():
            out[mask_head] = self.head_emb(x[mask_head])
            
        # Nhóm Mid: Tra cứu -> Đưa qua lớp Linear để phóng to lên 64 chiều
        if mask_mid.any():
            mid_embs = self.mid_emb(x[mask_mid])
            out[mask_mid] = self.proj_mid(mid_embs)
            
        # Nhóm Tail: Tra cứu -> Đưa qua lớp Linear để phóng to lên 64 chiều
        if mask_tail.any():
            # Paper gốc không dùng Hash cho Tail mà dùng bảng Exact Dimension nhỏ
            # ID của tail cần được dịch về từ 0 -> num_tail - 1 trong khâu tiền xử lý
            tail_embs = self.tail_emb(x[mask_tail])
            out[mask_tail] = self.proj_tail(tail_embs)
            
        return out