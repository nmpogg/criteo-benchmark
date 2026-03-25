# Review Paper: Fusion Matters: Learning Fusion in Deep Click-through Rate Prediction Models

**ArXiv ID:** [2411.15731](https://arxiv.org/abs/2411.15731)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết khoảng trống trong thiết kế CTR modeling:
- Các thành phần tương tác đặc trưng được phát triển kỹ, nhưng fusion design bị bỏ qua
- Thay đổi fusion design có thể dẫn đến hiệu suất khác nhau

## 2. Phương pháp sử dụng

- OptFusion: tự động hóa fusion learning thông qua connection learning + operation selection
- One-shot learning algorithm xử lý cả hai công việc đồng thời
- Tránh không gian tìm kiếm kém hiệu quả của NAS

## 3. Thành tựu đạt được

- Framework automated fusion learning tổng quát
- Xác thực trên 3 large-scale datasets
- Được chấp nhận tại WSDM 2025

## 4. Hạn chế

- Phương pháp fusion trước đó vẫn chưa được giải quyết hoàn toàn
- Hiệu quả tính toán so với NAS không rõ ràng
