import torch
import torch.nn as nn

class DeepFM(nn.Module):
    def __init__(self, num_dense_features, vocab_sizes, embed_dim, hidden_dims):
        super(DeepFM, self).__init__()
        self.num_sparse_features = len(vocab_sizes)
        self.num_dense_features = num_dense_features
        
        # 1. Thành phần FM bậc 1 (Linear)
        # Bậc 1 cho Sparse
        self.fm_1st_sparse = nn.ModuleList([nn.Embedding(vocab, 1) for vocab in vocab_sizes])
        # Bậc 1 cho Dense
        if num_dense_features > 0:
            self.fm_1st_dense = nn.Linear(num_dense_features, 1)
        
        # 2. Thành phần FM bậc 2 (Dùng chung embedding với Deep Component)
        self.embeddings = nn.ModuleList([nn.Embedding(vocab, embed_dim) for vocab in vocab_sizes])
        
        # 3. Thành phần Deep
        # Đầu vào của Deep là nối của tất cả Sparse Embeddings và Dense features
        deep_in_dim = (self.num_sparse_features * embed_dim) + num_dense_features
        deep_layers = []
        in_dim = deep_in_dim
        for dim in hidden_dims:
            deep_layers.append(nn.Linear(in_dim, dim))
            deep_layers.append(nn.ReLU())
            in_dim = dim
        deep_layers.append(nn.Linear(in_dim, 1))
        self.deep_net = nn.Sequential(*deep_layers)

    def forward(self, dense_x, sparse_x):
        # --- 1. FM: Tương tác bậc 1 ---
        fm_1st = sum([self.fm_1st_sparse[i](sparse_x[:, i]) for i in range(self.num_sparse_features)])
        if self.num_dense_features > 0:
            fm_1st = fm_1st + self.fm_1st_dense(dense_x)
        
        # --- 2. Lấy Embeddings chung ---
        emb_x = [self.embeddings[i](sparse_x[:, i]) for i in range(self.num_sparse_features)]
        emb_tensor = torch.stack(emb_x, dim=1) 
        
        # --- 3. FM: Tương tác bậc 2 ---
        sum_of_emb = torch.sum(emb_tensor, dim=1)
        sum_of_emb_sq = sum_of_emb ** 2
        sq_of_emb = emb_tensor ** 2
        sum_of_sq_emb = torch.sum(sq_of_emb, dim=1)
        fm_2nd = 0.5 * torch.sum(sum_of_emb_sq - sum_of_sq_emb, dim=1, keepdim=True)
        
        # --- 4. Deep Component ---
        deep_in = emb_tensor.view(sparse_x.size(0), -1) 
        if self.num_dense_features > 0:
            deep_in = torch.cat([dense_x, deep_in], dim=1) 
            
        deep_out = self.deep_net(deep_in)
        
        out = fm_1st + fm_2nd + deep_out
        return out.squeeze(1)