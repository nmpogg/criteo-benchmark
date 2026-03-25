# Review Paper: HoME: Hierarchy of Multi-Gate Experts for Multi-Task Learning at Kuaishou

**ArXiv ID:** [2408.05430](https://arxiv.org/abs/2408.05430)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Phát hiện 3 anomaly trong MoE của industry:
- Expert Collapse: 90%+ zero activation
- Expert Degradation: shared experts trở task-specific
- Expert Underfitting: sparse-data tasks bỏ qua specific experts

## 2. Phương pháp sử dụng

- HoME: hierarchical multi-gate expert framework
- Thiết kế cân bằng, hiệu quả MoE system
- Xử lý hàng chục concurrent prediction tasks

## 3. Thành tựu đạt được

- Cân bằng expert utilization, duy trì efficiency ở quy mô lớn
- Giải pháp thực tế Kuaishou short-video recommendation

## 4. Hạn chế

- Paper "Work in progress" (tháng 8/2024)
- Phát triển & đánh giá chưa hoàn toàn
