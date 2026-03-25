# Review Paper: GenCI: Generative Modeling of User Interest Shift via Cohort-based Intent Learning for CTR Prediction

**ArXiv ID:** [2601.18251](https://arxiv.org/abs/2601.18251)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết hai thách thức chính trong CTR prediction:
- Discriminative models bị overfitting trên historical features và không thích ứng với interest shifts
- Mất tín hiệu ngữ cảnh khi scoring candidates individually
- Đề xuất framework generative sử dụng "semantic interest cohorts" để mô hình hóa dynamic user preferences

## 2. Phương pháp sử dụng

Two-stage approach:
- Giai đoạn 1: Sinh ra explicit, candidate-agnostic interest cohorts thông qua generative modeling với next-item prediction objectives
- Giai đoạn 2: Refine representations thông qua candidate-aware network sử dụng cross-attention mechanisms
- Incorporates contextual signals thông qua hierarchical candidate-aware network
- End-to-end training để align user history, immediate intent, và target items

## 3. Thành tựu đạt được

- Framework generative hoạt động hiệu quả trên ba widely-used datasets
- Chứng minh alignment tốt hơn giữa user history, immediate intent, và target items
- Chấp nhận tại WWW 2026 Research Track

## 4. Hạn chế

- Không nêu rõ kết quả định lượng cụ thể (improvements percentage) trong abstract
- Chưa so sánh chi tiết với các baselines cụ thể trong mô tả
- Generative approach có thể tốn chi phí tính toán cao hơn discriminative models
