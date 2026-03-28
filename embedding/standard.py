import torch
import torch.nn as nn

class StandardEmbedding(nn.Module):
    def __init__(self, total_categories, embedding_dim=64):
        """
        total_categories: Tổng số lượng ID (Ví dụ: 1,000,000)
        """
        super(StandardEmbedding, self).__init__()
        # Cấp phát 1 bảng khổng lồ duy nhất
        self.emb = nn.Embedding(total_categories, embedding_dim)

    def forward(self, x, frequency_groups=None):
        """
        x: Tensor chứa các ID [batch_size]
        frequency_groups: Bỏ qua ở mô hình này vì không phân nhóm
        """
        return self.emb(x)