# Review Paper: MDL: Multi-Distribution Learning for Industrial Recommendations

**ArXiv ID:** [2602.07520](https://arxiv.org/abs/2602.07520)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện large-scale recommendation systems xử lý multi-scenario & multi-task learning:
- Underutilization của large-scale model parameters
- Difficulty trong jointly modeling scenario & task information
- Tối ưu distribution prediction cho multiple domains

## 2. Phương pháp sử dụng

MDL Framework: Lấy inspiration từ language models, treats scenarios & tasks như specialized tokens:
- Feature Token Self-Attention: Interaction richness
- Domain-Feature Attention: Adaptive feature activation
- Domain-Fused Aggregation: Distribution prediction
- Token-based paradigm cho scenario & task modeling

## 3. Thành tựu đạt được

- Testing on Douyin Search platform (production):
  - +0.0626% improvement trong LT30
  - -0.3267% reduction trong change query rate
- Deployed in production, phục vụ hundreds of millions users daily
- Effective parameter utilization cho multi-scenario learning

## 4. Hạn chế

- Token-based approach có thể add overhead cho inference
- Multi-distribution learning complexity - khó tune hyperparameters
- Evaluation metrics (LT30, change query rate) khá domain-specific
- Scaling tới many scenarios chưa được kiểm chứng rõ ràng
