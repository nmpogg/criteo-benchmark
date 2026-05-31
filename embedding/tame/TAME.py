import torch
import torch.nn as nn

class TAME_Embedding(nn.Module):
    """
    TAME: Target-Aware Memory-efficient Embedding Layer.
    Sử dụng Positional Sum-Routing để chập 6 không gian chiều lại làm 1,
    giữ nguyên số lượng đặc trưng là 26 cột, loại bỏ hoàn toàn lạm phát.
    """
    def __init__(self, vocab_sizes, target_dim=64):
        super(TAME_Embedding, self).__init__()
        self.target_dim = target_dim
        self.supported_dims = [64, 32, 16, 8, 4, 2]
        self.embedding_blocks = nn.ModuleDict()
        
        for dim in self.supported_dims:
            dim_str = str(dim)
            if dim_str in vocab_sizes and vocab_sizes[dim_str] > 0:
                self.embedding_blocks[dim_str] = nn.Embedding(
                    num_embeddings=vocab_sizes[dim_str] + 1, 
                    embedding_dim=dim,
                    padding_idx=0
                )

    def forward(self, grouped_inputs): #dict of {dim_str: [Batch, 26]}
        final_output = 0 
        
        for dim in self.supported_dims:
            dim_str = str(dim)
            if dim_str in grouped_inputs and dim_str in self.embedding_blocks:
                x = grouped_inputs[dim_str]
                emb = self.embedding_blocks[dim_str](x)
                
                # Mean-Scaled Tiling (Zero-Flop)
                if dim == self.target_dim:
                    out = emb
                else:
                    n_repeats = self.target_dim // dim
                    out = emb.repeat(1, 1, n_repeats) / n_repeats
                    
                # cộng chập
                final_output = final_output + out
        
        # output [Batch, 26, 64]
        return final_output