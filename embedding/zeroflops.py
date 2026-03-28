import torch
import torch.nn as nn
import torch.nn.functional as F

class ZeroFlopHybridEmbedding(nn.Module):
    def __init__(self, num_head, num_mid, hash_buckets, dim_head=64, dim_mid=32, dim_tail=16):
        super(ZeroFlopHybridEmbedding, self).__init__()
        self.dim_head = dim_head
        
        # 1. Bảng cho Head
        self.head_emb = nn.Embedding(num_head, dim_head)
        # 2. Bảng cho Mid (kích thước vector bằng một nửa)
        self.mid_emb = nn.Embedding(num_mid, dim_mid)
        # 3. Bảng Hash cho Tail (kích thước vector bằng 1/4)
        self.tail_emb = nn.Embedding(hash_buckets, dim_tail)
        self.hash_buckets = hash_buckets

    def forward(self, x, frequency_groups):
        """
        x: Tensor chứa ID [batch_size]
        frequency_groups: Tensor nhãn nhóm 0 (Head), 1 (Mid), 2 (Tail)
        """
        batch_size = x.size(0)
        # Khởi tạo ma trận kết quả với chuẩn dim = 64
        out = torch.zeros(batch_size, self.dim_head, device=x.device)
        
        # Mask cho từng nhóm
        mask_head = (frequency_groups == 0)
        mask_mid = (frequency_groups == 1)
        mask_tail = (frequency_groups == 2)
        
        # 1. Xử lý Head: Gán thẳng
        if mask_head.any():
            out[mask_head] = self.head_emb(x[mask_head])
            
        # 2. Xử lý Mid: Zero-Padding (Thêm 32 số 0 vào sau vector 32 chiều)
        if mask_mid.any():
            mid_vecs = self.mid_emb(x[mask_mid])
            # F.pad(tensor, (pad_left, pad_right))
            pad_size = self.dim_head - mid_vecs.size(1) 
            padded_vecs = F.pad(mid_vecs, (0, pad_size), "constant", 0)
            out[mask_mid] = padded_vecs
            
        # 3. Xử lý Tail: Hash + Tiling (Lặp lại vector 16 chiều thành 64)
        if mask_tail.any():
            hashed_ids = x[mask_tail] % self.hash_buckets
            tail_vecs = self.tail_emb(hashed_ids)
            # Tính toán số lần cần lặp: 64 // 16 = 4 lần
            repeats = self.dim_head // tail_vecs.size(1)
            tiled_vecs = tail_vecs.repeat(1, repeats)
            out[mask_tail] = tiled_vecs
            
        return out