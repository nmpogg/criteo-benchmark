import torch
import torch.nn as nn


class DHEEncoder(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        embed_dim: int,
        num_hashes: int = 1024,
        hidden_dims: tuple[int, ...] = (512, 256),
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.num_hashes = num_hashes
        self.embed_dim = embed_dim

        torch.manual_seed(42)
        self.register_buffer(
            "a_vec",
            torch.randint(1, 2**31 - 1, (num_hashes,), dtype=torch.long),
        )
        self.register_buffer(
            "b_vec",
            torch.randint(0, 2**31 - 1, (num_hashes,), dtype=torch.long),
        )
        self.p = 2**31 - 1

        layers: list[nn.Module] = []
        in_dim = num_hashes
        for hidden_dim in hidden_dims:
            layers.extend(
                [
                    nn.Linear(in_dim, hidden_dim),
                    nn.LayerNorm(hidden_dim),
                    nn.GELU(),
                ]
            )
            in_dim = hidden_dim
        layers.append(nn.Linear(in_dim, embed_dim))
        self.mlp = nn.Sequential(*layers)

    def _hash_encode(self, ids: torch.Tensor) -> torch.Tensor:
        batch_size = ids.size(0)
        ids_expanded = ids.unsqueeze(1).expand(batch_size, self.num_hashes)
        hashed = ((self.a_vec * ids_expanded + self.b_vec) % self.p) % 2
        return hashed.float() * 2 - 1

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        return self.mlp(self._hash_encode(ids))


class DHELayer(nn.Module):
    def __init__(
        self,
        vocab_sizes: list[int],
        embed_dim: int,
        num_hashes: int,
        hidden_dims: tuple[int, ...],
    ):
        super().__init__()
        self.encoders = nn.ModuleList(
            [
                DHEEncoder(vocab_size, embed_dim, num_hashes, hidden_dims)
                for vocab_size in vocab_sizes
            ]
        )
        self.embed_dim = embed_dim

    def forward(self, cat_x: torch.Tensor) -> torch.Tensor:
        embeddings = [
            encoder(cat_x[:, index])
            for index, encoder in enumerate(self.encoders)
        ]
        return torch.stack(embeddings, dim=1)


class Log1pNormalizer(nn.Module):
    def __init__(self, num_features: int):
        super().__init__()
        self.norm = nn.LayerNorm(num_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_log = torch.log1p(torch.abs(x)) * torch.sign(x)
        return self.norm(x_log)


class CrossNetwork(nn.Module):
    def __init__(self, input_dim: int, num_layers: int):
        super().__init__()
        self.num_layers = num_layers
        self.w = nn.ParameterList(
            [nn.Parameter(torch.empty(input_dim)) for _ in range(num_layers)]
        )
        self.b = nn.ParameterList(
            [nn.Parameter(torch.zeros(input_dim)) for _ in range(num_layers)]
        )
        for weight in self.w:
            nn.init.xavier_uniform_(weight.unsqueeze(0))

    def forward(self, x0: torch.Tensor) -> torch.Tensor:
        xl = x0
        for index in range(self.num_layers):
            xlw = (xl * self.w[index]).sum(dim=1, keepdim=True)
            xl = x0 * xlw + self.b[index] + xl
        return xl


class DCN_DHE(nn.Module):
    def __init__(
        self,
        num_dense: int,
        vocab_sizes: list[int],
        embed_dim: int,
        cross_layers: int,
        hidden_dims: tuple[int, ...],
        dhe_num_hashes: int,
        dhe_hidden: tuple[int, ...],
    ):
        super().__init__()
        self.num_dense = num_dense
        self.num_sparse = len(vocab_sizes)
        self.embed_dim = embed_dim

        self.dense_norm = Log1pNormalizer(num_dense)
        self.dhe = DHELayer(vocab_sizes, embed_dim, dhe_num_hashes, dhe_hidden)

        input_dim = num_dense + self.num_sparse * embed_dim
        self.cross_net = CrossNetwork(input_dim, cross_layers)

        deep_layers: list[nn.Module] = []
        in_dim = input_dim
        for hidden_dim in hidden_dims:
            deep_layers.extend(
                [
                    nn.Linear(in_dim, hidden_dim),
                    nn.LayerNorm(hidden_dim),
                    nn.GELU(),
                    nn.Dropout(0.1),
                ]
            )
            in_dim = hidden_dim
        self.deep_net = nn.Sequential(*deep_layers)
        self.fc = nn.Linear(input_dim + in_dim, 1)

    def forward(self, dense_x: torch.Tensor, sparse_x: torch.Tensor) -> torch.Tensor:
        dense_norm = self.dense_norm(dense_x)
        embeddings = self.dhe(sparse_x)
        embeddings_flat = embeddings.view(dense_x.size(0), -1)

        x0 = torch.cat([dense_norm, embeddings_flat], dim=1)
        cross_out = self.cross_net(x0)
        deep_out = self.deep_net(x0)
        combined = torch.cat([cross_out, deep_out], dim=1)
        return self.fc(combined)
