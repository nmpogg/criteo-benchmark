# Review Paper: Two-Dimensional Sparse Parallelism for DLRM Training with Trillion-Parameter Embeddings

**ArXiv ID:** [2508.03854](https://arxiv.org/abs/2508.03854)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Đạt khả năng mở rộng cho training DLRMs với embedding tables hàng triệu tham số:
- Trên các GPU cluster khổng lồ (lên tới 4000 GPUs)

## 2. Phương pháp sử dụng

- 2D sparse parallelism: model parallelism + data parallelism
- Momentum-scaled row-wise AdaGrad algorithm để ngăn suy giảm hiệu suất
- Tối ưu hóa xử lý imbalance, straggler issues, communication overhead

## 3. Thành tựu đạt được

- Đạt nearly linear training speed scaling lên tới 4000 GPUs
- Giữ nguyên hiệu suất mô hình
- Benchmark mới cho efficient recommendation model training

## 4. Hạn chế

- Chỉ giới hạn trên DLRM
- Khả năng áp dụng cho các loại mô hình khác không rõ
- Không chi tiết các trade-offs cụ thể
