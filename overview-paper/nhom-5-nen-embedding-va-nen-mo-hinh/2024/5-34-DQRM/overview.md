# Review Paper: DQRM: Deep Quantized Recommendation Models - INT4 Quantization

**ArXiv ID:** [2410.20046](https://arxiv.org/abs/2410.20046)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding tables khổng lồ (1TB+) tạo chai lỏ bộ nhớ:
- Mục tiêu: giảm từ 2TB+ xuống cỡ GB mà không mất độ chính xác

## 2. Phương pháp sử dụng

- Quantization-Aware Training (QAT) cho INT4 quantization toàn bộ DLRM
- Hai kỹ thuật mới cải thiện QAT cho embedding tables
- INT8 gradient quantization + sparsification cho distributed training

## 3. Thành tựu đạt được

- INT4 quantization mà không mất độ chính xác
- Kaggle: 79.07% accuracy, 0.27GB (vs 2.16GB FP32) → ~8x compression
- Terabyte: 81.21% accuracy, 1.57GB (vs 12.58GB) → ~8x compression

## 4. Hạn chế

- Chưa rõ hiệu suất trên inference edge devices
- Không thảo luận chi phí training với QAT
