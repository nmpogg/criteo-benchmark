# Review Paper: UIST: Discrete Semantic Tokenization for Deep CTR Prediction

**ArXiv ID:** [2403.08206](https://arxiv.org/abs/2403.08206)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Tích hợp thông tin nội dung item vào mô hình CTR prediction:
- Cân bằng hiệu suất tính toán và giới hạn bộ nhớ trong môi trường công nghiệp

## 2. Phương pháp sử dụng

- Lượng tử hóa dense embedding vectors thành các token rời rạc
- Hierarchical mixture inference module để cân nặng đóng góp user-item token pair

## 3. Thành tựu đạt được

- Nén không gian ~200x mà duy trì tốc độ training và inference nhanh
- Hiệu quả trên news recommendation systems

## 4. Hạn chế

- Tập trung vào news recommendation → độ tổng quát có hạn
- Không thảo luận chi tiết về mất thông tin trong tokenization
