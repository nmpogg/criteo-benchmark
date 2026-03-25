# Review Paper: FCN: Fusing Exponential and Linear Cross Network for Click-Through Rate Prediction (DCNv3)

**ArXiv ID:** [2407.13349](https://arxiv.org/abs/2407.13349)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện mô hình Deep & Cross Network (DCN) cho dự đoán CTR:
- Phương pháp tương tác đặc trưng tường minh không tốt như DNN ẩn
- Mô hình bỏ qua nhiễu trong các tương tác bậc cao
- Thiếu tín hiệu giám sát riêng cho các nhánh mạng
- Tương tác bậc cao không rõ ràng, khó diễn giải

## 2. Phương pháp sử dụng

- Linear Cross Network (LCN) + Exponential Cross Network (ECN) mô hình hóa tương tác với tăng trưởng tuyến tính và hàm mũ
- Self-Mask operation: lọc nhiễu từng lớp, giảm 50% tham số
- Tri-BCE loss: hàm mất mát cung cấp tín hiệu giám sát riêng cho từng mạng

## 3. Thành tựu đạt được

- SOTA trên 6 benchmark datasets
- Cải thiện khả năng diễn giải, hiệu quả tính toán
- Loại bỏ phụ thuộc vào DNN ẩn
- Được chấp nhận tại KDD'26

## 4. Hạn chế

- Không rõ khả năng mở rộng với dữ liệu thực tế cực lớn
- Phức tạp tính toán Self-Mask operation chưa được phân tích chi tiết
