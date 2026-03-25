# Review Paper: Helen: Optimizing CTR Prediction Models with Frequency-wise Hessian Eigenvalue Regularization

**ArXiv ID:** [2403.00798](https://arxiv.org/abs/2403.00798)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Tiếp cận CTR prediction từ góc độ tối ưu hóa:
- Đặc trưng xuất hiện thường xuyên có xu hướng hội tụ về cực tiểu sắc nét (sharp local minima)
- Dẫn đến hiệu suất kém

## 2. Phương pháp sử dụng

- Helen optimizer: kết hợp chính quy hóa eigenvalue Hessian theo tần suất đặc trưng
- Dựa trên sharpness-aware minimization principles
- Perturbation thích ứng dựa trên tần suất đặc trưng chuẩn hóa
- Kiểm tra trên 7 mô hình, 3 benchmark datasets

## 3. Thành tựu đạt được

- Xác định vấn đề tối ưu hóa cơ bản trong CTR prediction
- Giới hạn thành công top Hessian eigenvalue
- Được chấp nhận tại WWW'24

## 4. Hạn chế

- Không cụ thể về cải thiện hiệu suất định lượng
- Chỉ đánh giá trong BARS benchmark
- Không so sánh với các optimizer khác ngoài optimizer chuẩn
