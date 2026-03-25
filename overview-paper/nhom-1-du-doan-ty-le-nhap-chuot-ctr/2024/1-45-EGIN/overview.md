# Review Paper: EGIN: Light-weight End-to-End Graph Interest Network for CTR Prediction in E-commerce Search

**ArXiv ID:** [2406.17745](https://arxiv.org/abs/2406.17745)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

CTR trong e-commerce search khác recommendation:
- Phương pháp hiện tại bỏ qua query & query-item relationships

## 2. Phương pháp sử dụng

- Query-item heterogeneous graph capture tương quan & thông tin tuần tự
- Light-weight graph sampling xử lý hiệu quả
- Multi-interest network dùng graph embeddings
- End-to-end training kết hợp graph embedding + CTR prediction

## 3. Thành tựu đạt được

- Lấp đầy khoảng cách recommendation vs search-specific CTR
- Chi phí training thấp
- Deployment thực tế hệ thống search lớn

## 4. Hạn chế

- Chỉ test trên dataset cụ thể
- Không thảo luận thách thức graph ở extreme scale
