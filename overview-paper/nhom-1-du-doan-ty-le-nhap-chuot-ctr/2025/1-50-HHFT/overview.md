# Review Paper: HHFT: Hierarchical Heterogeneous Feature Transformer for Recommendation Systems

**ArXiv ID:** [2511.20235](https://arxiv.org/abs/2511.20235)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Xử lý giới hạn của DNN truyền thống trong CTR prediction:
- Phát triển kiến trúc Transformer để xử lý tốt hơn các đặc trưng không đồng nhất
- Tập trung vào cấu trúc khối đặc trưng semantic

## 2. Phương pháp sử dụng

- Semantic Feature Partitioning: nhóm các đặc trưng đa dạng thành các khối coherent
- Heterogeneous Transformer Encoder: sử dụng QKV projections và FFN riêng theo khối
- Hiformer Layer: nắm bắt tương tác đặc trưng cấp cao

## 3. Thành tựu đạt được

- +0.4% cải thiện CTR AUC so với DNN baselines ở quy mô lớn
- +0.6% tăng GMV trong triển khai thực tế
- Triển khai thành công trên nền tảng Taobao

## 4. Hạn chế

- Chưa thảo luận về trade-off, độ phức tạp hoặc hạn chế
- Kết quả chủ yếu từ Taobao, tổng quát hóa chưa rõ
- Không so sánh với các Transformer-based methods khác
