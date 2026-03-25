# Review Paper: CETNet: A Collaborative Ensemble Framework for CTR Prediction

**ArXiv ID:** [2411.13700](https://arxiv.org/abs/2411.13700)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện khả năng mở rộng hệ thống khuyến nghị:
- Sử dụng nhiều mô hình khác biệt để nắm bắt các mẫu tương tác khác nhau
- Thay vì chỉ tăng kích thước mô hình

## 2. Phương pháp sử dụng

- CETNet: ensemble framework với nhiều mô hình độc lập, embedding tables riêng
- Collaborative learning: các mô hình lặp lại để tinh chỉnh dự đoán
- Confidence-based fusion mechanism: softmax với negation entropy
- Đánh giá trên 5 datasets (3 công khai + Meta industrial + Criteo, Avazu)

## 3. Thành tựu đạt được

- Entropy-based confidence weighting cân bằng động đóng góp mô hình
- Hiệu suất tương đương/cao hơn với embedding dimensions nhỏ hơn
- Xác thực trên nhiều large-scale datasets

## 4. Hạn chế

- So sánh chủ yếu với mô hình riêng lẻ
- Chi phí tính toán duy trì nhiều mô hình chưa được phân tích
