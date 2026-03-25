# Review Paper: InterFormer: Effective Heterogeneous Interaction Learning for CTR Prediction

**ArXiv ID:** [2411.09852](https://arxiv.org/abs/2411.09852)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện tích hợp các nguồn thông tin dị thể cho CTR prediction:
- Tương tác giữa các loại dữ liệu không đủ do lưu lượng thông tin đơn hướng
- Mất thông tin từ tổng hợp sớm

## 2. Phương pháp sử dụng

- InterFormer module: bidirectional information flow giữa các mode
- Separate bridging arch: lựa chọn và tóm tắt thông tin hiệu quả
- Tránh tổng hợp sớm: duy trì thông tin đầy đủ trước tóm tắt chọn lọc

## 3. Thành tựu đạt được

- SOTA trên 3 public datasets + 1 industrial dataset
- Giải quyết tương tác inter-mode không đủ
- Giảm mất thông tin

## 4. Hạn chế

- Độ phức tạp tính toán của bridging arch chưa được phân tích
- Khả năng mở rộng đến hàng triệu user-item pairs chưa kiểm tra
