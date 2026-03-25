# Review Paper: Enhancing CTR Prediction with De-correlated Expert Networks

**ArXiv ID:** [2505.17925](https://arxiv.org/abs/2505.17925)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Xem xét cơ chế Mixture-of-Experts (MoE) trong CTR prediction, khám phá liệu các chiến lược MoE hiện tại có tạo ra các expert đủ khác biệt, không tương quan.
- Tập trung vào mô hình hóa tương tác đặc trưng cho dự đoán click-through rate trong quảng cáo

## 2. Phương pháp sử dụng

- Framework De-Correlated MoE (D-MoE) với Cross-Expert De-Correlation loss
- Metric "Cross-Expert Correlation" để đo lường sự khác biệt giữa các expert
- Áp dụng liên tiếp nhiều chiến lược de-correlation
- A/B testing trực tuyến trên nền tảng quảng cáo của Tencent

## 3. Thành tựu đạt được

- Chứng minh các chiến lược de-correlation tương thích lẫn nhau, áp dụng liên tiếp dẫn đến giảm tương quan và tăng hiệu suất
- Đạt lift +1.19% GMV so với Multi-Embedding MoE baseline trong kiểm thử sản xuất

## 4. Hạn chế

- Chỉ xác thực trên nền tảng Tencent, khả năng tổng quát hóa chưa rõ
- Không chi tiết về độ phức tạp tính toán hoặc chi phí triển khai
