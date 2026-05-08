import torch
import torch.nn as nn

class DLRM(nn.Module):
    def __init__(self, num_dense_features, vocab_sizes, embed_dim, bottom_mlp_dims, top_mlp_dims):
        super(DLRM, self).__init__()
        self.embeddings = nn.ModuleList([nn.Embedding(vocab, embed_dim) for vocab in vocab_sizes])
        
        # Bottom MLP xử lý Dense features
        bottom_layers = []
        in_dim = num_dense_features
        for dim in bottom_mlp_dims:
            bottom_layers.append(nn.Linear(in_dim, dim))
            bottom_layers.append(nn.ReLU())
            in_dim = dim
        self.bottom_mlp = nn.Sequential(*bottom_layers)
        
        assert bottom_mlp_dims[-1] == embed_dim, "Output của Bottom MLP phải bằng với embed_dim"
        
        # Tính toán số chiều đầu vào cho Top MLP
        num_sparse = len(vocab_sizes)
        # Bao gồm: output dense + các cặp tương tác (dot products)
        interaction_dim = embed_dim + ((num_sparse + 1) * num_sparse) // 2
        
        # Top MLP
        top_layers = []
        in_dim = interaction_dim
        for dim in top_mlp_dims:
            top_layers.append(nn.Linear(in_dim, dim))
            top_layers.append(nn.ReLU())
            in_dim = dim
        top_layers.append(nn.Linear(in_dim, 1))
        self.top_mlp = nn.Sequential(*top_layers)

    def forward(self, dense_x, sparse_x):
        # 1. Đi qua Bottom MLP
        dense_out = self.bottom_mlp(dense_x) # (batch, embed_dim)
        
        # 2. Embeddings
        emb_x = [emb(sparse_x[:, i]) for i, emb in enumerate(self.embeddings)]
        
        # Đưa thêm kết quả của dense_out vào danh sách để tính tương tác chung
        emb_x.append(dense_out) 
        stacked_emb = torch.stack(emb_x, dim=1) # (batch, num_sparse + 1, embed_dim)
        
        # 3. Tính Interactions (Dot products)
        # Sử dụng Batch Matrix Multiplication (bmm)
        interaction_matrix = torch.bmm(stacked_emb, stacked_emb.transpose(1, 2))
        
        # Lấy phần tam giác trên của ma trận tương tác (không tính đường chéo)
        num_features = stacked_emb.size(1)
        row_idx, col_idx = torch.triu_indices(num_features, num_features, offset=1)
        interactions = interaction_matrix[:, row_idx, col_idx]
        
        # 4. Nối (concat) original dense_out với vector interactions
        concat_x = torch.cat([dense_out, interactions], dim=1)
        
        # 5. Đi qua Top MLP
        out = self.top_mlp(concat_x)
        return  out.squeeze(1)