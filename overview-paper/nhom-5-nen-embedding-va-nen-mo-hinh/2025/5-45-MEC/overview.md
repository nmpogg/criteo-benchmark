# Review Paper: A Universal Framework for Compressing Embeddings in CTR Prediction (MEC)

**ArXiv ID:** [2502.15355](https://arxiv.org/abs/2502.15355)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết inefficiency bộ nhớ trong CTR prediction:
- Embedding tables quá lớn, vượt quá GPU memory limits
- Gây latency cao từ data transfer GPU ↔ CPU

## 2. Phương pháp sử dụng

- Model-agnostic Embedding Compression (MEC) framework
- Hai giai đoạn:
  1. Popularity-weighted regularization: cân bằng code distribution
  2. Contrastive learning: đảm bảo uniform distribution quantized codes

## 3. Thành tựu đạt được

- Giảm memory sử dụng > 50×
- Duy trì hoặc cải thiện recommendation performance
- Kiểm tra trên 3 datasets
- Model-agnostic (áp dụng được rộng)

## 4. Hạn chế

- Ít chi tiết về trade-offs hiệu suất
- Không rõ computational overhead trong quá trình nén
- Tập trung vào embedding compression, không xem xét system-level
