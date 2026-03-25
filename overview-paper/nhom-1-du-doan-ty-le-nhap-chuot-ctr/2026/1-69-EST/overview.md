# Review Paper: EST: Towards Efficient Scaling Laws in Click-Through Rate Prediction via Unified Modeling

**ArXiv ID:** [2602.10811](https://arxiv.org/abs/2602.10811)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết vấn đề scaling hiệu quả các mô hình CTR prediction:
- Các phương pháp hiện tại mất mát tín hiệu fine-grained thông qua early aggregation của user behaviors
- Tìm cách xây dựng stable power-law scaling cho CTR models

## 2. Phương pháp sử dụng

EST (Efficiently Scalable Transformer) với hai thành phần chính:
- Lightweight Cross-Attention (LCA): Loại bỏ self-interactions dư thừa, tập trung vào feature relationships quan trọng
- Content Sparse Attention (CSA): Sử dụng content similarity để xác định và ưu tiên behavioral signals có giá trị cao
- Xử lý raw inputs như một unified sequence mà không mất thông tin

## 3. Thành tựu đạt được

- Thiết lập stable power-law scaling cho CTR prediction models
- Triển khai thành công trên platform quảng cáo Taobao:
  - +3.27% RPM (Revenue Per Mile)
  - +1.22% CTR lift
- Tạo khung work thực tế cho scaling industrial CTR models

## 4. Hạn chế

- Chủ yếu đánh giá trên single platform (Taobao) - generalization cần xác minh thêm
- Yêu cầu tính toán vẫn còn khá cao cho multi-head attention
- Chưa rõ performance với extreme long sequences
