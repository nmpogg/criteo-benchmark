# Review Paper: DGIN: Deep Group Interest Modeling of Full Lifelong User Behaviors for CTR Prediction

**ArXiv ID:** [2311.10764](https://arxiv.org/abs/2311.10764)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Mô hình hóa toàn bộ lịch sử hành vi user (clicks, cart additions, purchases) cho CTR prediction:
- Không chỉ clicks mà tất cả behavior types

## 2. Phương pháp sử dụng

- Group behavior sequences theo relevant keys: giảm O(10^4) → O(10^2)
- Capture group attributes qua statistical measures + self-attention
- Transformer để derive user interests từ reorganized behavior data

## 3. Thành tựu đạt được

- End-to-end approach giải quyết information loss trong two-stage methods
- Hiệu suất & efficiency tối ưu trên industrial & public datasets
- Xử lý long behavior sequences

## 4. Hạn chế

- Trade-off giữa efficiency gains từ grouping và information loss
- Không rõ performance trên sequences rất dài (O(10^5)+)
- Complexity trong implementation & tuning
