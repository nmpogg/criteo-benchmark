import torch
import torch.nn as nn

class CrossNetwork(nn.Module):
    def __init__(self, input_dim, num_layers):
        super(CrossNetwork, self).__init__()
        self.num_layers = num_layers
        # Trọng số và bias cho mỗi lớp cross
        self.cross_weights = nn.ParameterList([nn.Parameter(torch.randn(input_dim)) for _ in range(num_layers)])
        self.cross_bias = nn.ParameterList([nn.Parameter(torch.zeros(input_dim)) for _ in range(num_layers)])

    def forward(self, x0):
        x_l = x0
        for i in range(self.num_layers):
            # Tính (x_l^T * w_l) -> scalar cho mỗi sample trong batch
            xl_w = torch.matmul(x_l, self.cross_weights[i])
            xl_w = xl_w.unsqueeze(1) 
            # Cập nhật: x_{l+1} = x_0 * (x_l^T * w_l) + b_l + x_l
            x_l = x0 * xl_w + self.cross_bias[i] + x_l
        return x_l

class DCN(nn.Module):
    def __init__(self, num_dense_features, sparse_vocab_sizes, embed_dim, cross_layers, hidden_dims):
        super(DCN, self).__init__()
        # Embedding cho sparse features
        self.embeddings = nn.ModuleList([nn.Embedding(vocab, embed_dim) for vocab in sparse_vocab_sizes])
        
        input_dim = num_dense_features + len(sparse_vocab_sizes) * embed_dim
        
        # Mạng Cross
        self.cross_net = CrossNetwork(input_dim, cross_layers)
        
        # Mạng Deep
        deep_layers = []
        in_dim = input_dim
        for dim in hidden_dims:
            deep_layers.append(nn.Linear(in_dim, dim))
            deep_layers.append(nn.ReLU())
            in_dim = dim
        self.deep_net = nn.Sequential(*deep_layers)
        
        # Lớp Combination để dự đoán cuối cùng (Output Layer)
        self.fc = nn.Linear(input_dim + in_dim, 1)

    def forward(self, dense_x, sparse_x):
        # Embedding các giá trị sparse
        emb_x = [emb(sparse_x[:, i]) for i, emb in enumerate(self.embeddings)]
        emb_x = torch.cat(emb_x, dim=1)
        
        # Nối (stack) dense features và embedded sparse features
        x0 = torch.cat([dense_x, emb_x], dim=1)
        
        # Đi qua 2 mạng song song
        cross_out = self.cross_net(x0)
        deep_out = self.deep_net(x0)
        
        # Nối đầu ra
        combined = torch.cat([cross_out, deep_out], dim=1)
        
        # Đi qua lớp Linear cuối cùng để lấy logits
        out = self.fc(combined)
        
        # Ép về 1D (bỏ sigmoid) để tương thích với BCEWithLogitsLoss
        return out.squeeze(1)