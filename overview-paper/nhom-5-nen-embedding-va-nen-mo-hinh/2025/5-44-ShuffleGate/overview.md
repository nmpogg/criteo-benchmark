# Review Paper: ShuffleGate: Scalable Feature Optimization for Recommender Systems via Batch-wise Sensitivity Learning

**ArXiv ID:** [2503.09315](https://arxiv.org/abs/2503.09315)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Xác định feature & embedding parameter nào essential vs redundant:
- Giảm dimensionality & tăng hiệu quả tính toán
- Cải thiện generalization của mô hình

## 2. Phương pháp sử dụng

- Batch-wise shuffling strategy để xóa thông tin end-to-end differentiable
- Ước tính component importance bằng cách đo lường response mô hình đến information loss
- Tạo naturally polarized importance scores

## 3. Thành tựu đạt được

- Prune 99.9% redundant embedding parameters trên Criteo dataset
- Hiệu suất cạnh tranh được duy trì
- Industrial deployment: 91% tăng training throughput
- Nén input dimensions từ 10,000+ → 1,000+
- Phục vụ hàng tỷ requests hằng ngày

## 4. Hạn chế

- Phạm vi chủ yếu là recommender systems
- Chi tiết kỹ thuật & constraint ở full paper
