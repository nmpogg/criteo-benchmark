# Review Paper: FSDNet: Feature Interaction Fusion Self-Distillation Network for CTR Prediction

**ArXiv ID:** [2411.07508](https://arxiv.org/abs/2411.07508)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết vấn đề tương tác feature trong CTR prediction:
- Cải thiện chia sẻ thông tin giữa các feature

## 2. Phương pháp sử dụng

- Plug-and-play fusion self-distillation module kết nối explicit & implicit feature interactions
- Deepest fusion layer làm teacher model hướng dẫn shallow layers
- Tăng cường chia sẻ thông tin cross-feature

## 3. Thành tựu đạt được

- Hiệu suất cải thiện trên 4 benchmark datasets
- Khả năng tổng quát hóa mạnh

## 4. Hạn chế

- Noise trong construction feature interactions
- Thách thức modeling high-order feature interactions
- Chi phí tính toán không rõ khi thêm distillation module
