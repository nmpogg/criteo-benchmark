# Review Paper: DMF: Decoupled Multimodal Fusion for User Interest Modeling in CTR Prediction

**ArXiv ID:** [2510.11066](https://arxiv.org/abs/2510.11066)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Tích hợp dữ liệu đa phương thức (văn bản, hình ảnh) với collaborative filtering dựa trên ID:
- Mô hình hiện tại xử lý các loại dữ liệu riêng rẽ
- Bỏ lỡ tương tác giữa ngữ nghĩa nội dung và tín hiệu hành vi người dùng

## 2. Phương pháp sử dụng

- DMF: strategy "modality-enriched modeling" tạo target-aware features
- Kết nối các embedding spaces khác nhau
- Cơ chế attention tối ưu hóa inference: decouples computations để giảm chi phí

## 3. Thành tựu đạt được

- Triển khai trên nền tảng e-commerce Lazada:
  - CTCVR +5.30% (relative)
  - GMV +7.43%
- Chi phí tính toán tối thiểu

## 4. Hạn chế

- Abstract không nêu rõ hạn chế
- Tập trung chủ yếu vào kết quả dương tính từ offline experiments và production metrics
