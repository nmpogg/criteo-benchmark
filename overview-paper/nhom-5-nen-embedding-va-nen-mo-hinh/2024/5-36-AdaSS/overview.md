# Review Paper: AdaS&S: Adaptive Shrinking & Splitting for Embedding Heterogeneity in Recommendation

**ArXiv ID:** [2411.07504](https://arxiv.org/abs/2411.07504)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Tự động lựa chọn kích thước embedding cho các đặc trưng phân loại:
- Phương pháp trước đây không ổn định và tốn bộ nhớ

## 2. Phương pháp sử dụng

- Supernet one-shot với Adaptive Sampling method
- Reinforcement Learning với resource competition penalty
- Cân bằng hiệu suất model vs. ràng buộc bộ nhớ

## 3. Thành tựu đạt được

- Cải thiện AUC ~0.3% đồng thời tiết kiệm ~20% tham số model
- Độ ổn định tìm kiếm vượt trội

## 4. Hạn chế

- Cải thiện AUC khiêm tốn (0.3%)
- Tính ổn định vẫn có biến động
