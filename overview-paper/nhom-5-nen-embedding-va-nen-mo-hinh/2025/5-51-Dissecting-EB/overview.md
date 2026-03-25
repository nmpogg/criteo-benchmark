# Review Paper: Dissecting Embedding Bag Performance in DLRM Inference: A Comprehensive Study on Multi-GPU Deployment

**ArXiv ID:** [2512.05831](https://arxiv.org/abs/2512.05831)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Phân tích chi tiết hiệu suất Embedding Bag kernels trong DLRMs khi phân tán trên nhiều GPUs:
- Bảng embedding lớn phải trải dài trên nhiều GPUs, gây overhead communication

## 2. Phương pháp sử dụng

- Đo lường hiệu suất Embedding Bag kernel trên H100 GPUs
- Sử dụng NCCL và NVSHMEM libraries
- Đánh giá qua: batch sizes, số lượng embedding tables, kích thước bảng, pooling factors, embedding dimensions

## 3. Thành tựu đạt được

- Cung cấp empirical performance projections cho phân tán large embedding tables
- Xác định scalability limitations và communication bottlenecks
- Benchmark cho H100 GPUs

## 4. Hạn chế

- Chỉ tập trung vào H100 GPUs; không tổng quát cho hardware khác
- Chủ yếu empirical/measurement-focused, không đề xuất giải pháp tối ưu mới
- Không cung cấp kỹ thuật mitigation
