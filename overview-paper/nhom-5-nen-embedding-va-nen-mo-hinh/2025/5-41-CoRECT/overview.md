# Review Paper: CoRECT: A Framework for Evaluating Embedding Compression Techniques at Scale

**ArXiv ID:** [2510.19340](https://arxiv.org/abs/2510.19340)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Đánh giá hệ thống các kỹ thuật nén embedding trong dense retrieval trên quy mô lớn (100M passages):
- Khám phá ảnh hưởng của độ phức tạp corpus đến hiệu suất nén
- Xây dựng framework đánh giá chuẩn

## 2. Phương pháp sử dụng

- CoRECT: framework đánh giá quy mô lớn + bộ dataset mới
- Benchmark 8 kiểu nén đại diện khác nhau
- Đánh giá hiệu suất theo các điều kiện & mô hình khác nhau

## 3. Thành tựu đạt được

- Chứng minh kỹ thuật nén không học (non-learned) đạt giảm kích thước index đáng kể
- Mất hiệu suất có thể bỏ qua về mặt thống kê
- Phương pháp đơn giản cạnh tranh với phương pháp phức tạp

## 4. Hạn chế

- Hiệu suất thay đổi đáng kể giữa các mô hình khác nhau
- Chọn phương pháp nén tối ưu vẫn còn khó khăn
