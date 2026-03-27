# Review Paper: FCN: Fusing Exponential and Linear Cross Network for Click-Through Rate Prediction (DCNv3)

**ArXiv ID:** [2407.13349](https://arxiv.org/abs/2407.13349)
**Năm:** 2024 | **Venue:** KDD 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết những giới hạn của Deep & Cross Network (DCN) trong dự đoán CTR. Các phương pháp tương tác tường minh (explicit) không hoạt động tốt bằng mạng sâu ngầm (implicit DNN), dẫn đến tận dụng không đầy đủ thông tin tương tác feature. Mô hình hiện tại bỏ qua nhiễu trong tương tác bậc cao, thiếu tín hiệu giám sát riêng cho từng nhánh mạng, và tương tác bậc cao khó diễn giải. FCN được đề xuất để kết hợp tường minh và ngầm hiệu quả mà không phụ thuộc vào DNN.

## 2. Phương pháp sử dụng

FCN sử dụng hai thành phần chính kết hợp:

- **Linear Cross Network (LCN)**: Mô hình hóa tương tác feature với tăng trưởng tuyến tính, xử lý tương tác bậc thấp hiệu quả
- **Exponential Cross Network (ECN)**: Mô hình hóa tương tác bậc cao với tăng trưởng hàm mũ, chi phí tính toán hiệu quả hơn DNN
- **Self-Mask operation**: Lọc nhiễu từng lớp (progressive noise filtering), giảm **50% tham số** so với DCN truyền thống
- **Tri-BCE loss**: Hàm mất mát cung cấp tín hiệu giám sát riêng cho từng nhánh (LCN + ECN), thay vì chỉ một loss chung

Kết hợp LCN + ECN loại bỏ phụ thuộc vào DNN ẩn mà vẫn đạt hiệu suất cao.

## 3. Thành tựu đạt được

- **SOTA trên 6 benchmark datasets**, cải thiện đáng kể về accuracy, efficiency, và interpretability
- Loại bỏ phụ thuộc vào DNN ẩn — explicit interactions đủ mạnh
- Self-Mask giảm 50% parameters mà không hy sinh hiệu suất
- Chấp nhận tại **KDD 2026** — hội nghị hàng đầu data mining

## 4. Hạn chế

- Hai mạng riêng biệt + custom loss tăng implementation complexity
- Scalability thực tế trên hệ thống production cực lớn chưa được kiểm chứng chi tiết
- Tuning hyperparameters cho LCN/ECN trên các dataset khác nhau chưa rõ hướng dẫn
- Chi phí bộ nhớ cho hai embedding tables và intermediate representations có thể tăng đáng kể
