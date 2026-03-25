# Review Paper: LAIN: Length-Adaptive Interest Network for Balancing Long and Short Sequence Modeling in CTR Prediction

**ArXiv ID:** [2601.19142](https://arxiv.org/abs/2601.19142)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết vấn đề: khi tăng sequence length, hiệu suất giảm với users có interaction history ngắn:
- Nhận diện mâu thuẫn: longer sequences cung cấp thêm context nhưng làm khó modeling short-term behaviors
- Mục tiêu: balance giữa long-sequence và short-sequence modeling

## 2. Phương pháp sử dụng

Length-Adaptive Interest Network (LAIN) với 3 thành phần:
- Spectral Length Encoder: Biến đổi sequence length thành continuous representations
- Length-Conditioned Prompting: Inject contextual information vào cả long-term và short-term branches
- Length-Modulated Attention: Điều chỉnh attention intensity dựa vào sequence length

## 3. Thành tựu đạt được

- AUC improvement: Lên tới 1.15%
- Log loss reduction: 2.25%
- Hiệu quả cho short-sequence users: Cải thiện đáng kể mà không xấu đi performance cho long-sequence users
- Test trên 3 real-world datasets với 5 baseline architectures
- Accepted to AAAI 2026

## 4. Hạn chế

- Spectral Length Encoding có thể không tối ưu cho tất cả distribution của sequence lengths
- Phương pháp length-modulated attention chưa rõ ràng cách điều chỉnh magnitude/strength
- Generalization tới các kiểu sequences (e.g., irregular timestamps) chưa được discussion
