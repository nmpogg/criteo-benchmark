# Review Paper: HiLoMoE: Hierarchical Low-Rank Mixture of Experts for Efficient CTR Model Scaling

**ArXiv ID:** [2510.10432](https://arxiv.org/abs/2510.10432)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết scaling challenges trong CTR prediction:
- Kết hợp vertical scaling (layer stacking) & horizontal scaling (MoE)
- Sequential layer-by-layer computation giới hạn efficiency

## 2. Phương pháp sử dụng

- HiLoMoE framework:
  - Lightweight rank-1 experts cho parameter-efficient expansion
  - Multiple stacked MoE layers với hierarchical routing
  - Parallel execution: routing dựa trên prior layer scores
  - 3-stage training: stable optimization & expert diversity

## 3. Thành tựu đạt được

- Average: +0.20% AUC improvement
- 18.5% FLOPs reduction vs baseline non-MoE models
- Better performance-efficiency tradeoffs
- Tested trên 4 public datasets

## 4. Hạn chế

- Modest AUC improvement (0.20%) relative to computational savings
- Hierarchical patterns assumption có thể không luôn đúng
- Scalability với extremely large models chưa validate
