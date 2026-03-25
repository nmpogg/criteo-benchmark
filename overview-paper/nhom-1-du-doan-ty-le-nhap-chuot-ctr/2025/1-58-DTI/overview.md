# Review Paper: DTI: Towards An Efficient LLM Training Paradigm for CTR Prediction

**ArXiv ID:** [2503.01001](https://arxiv.org/abs/2503.01001)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết inefficiency trong việc training LLMs cho CTR prediction:
- High training costs khi apply LLMs vào ranking-based recommendation systems
- Với large interaction sequences

## 2. Phương pháp sử dụng

- Dynamic Target Isolation (DTI): Novel training paradigm
- Structurally parallelize training của k (k >> 1) target interactions
- Giải quyết 2 bottlenecks: hidden-state leakage & positional bias overfitting

## 3. Thành tựu đạt được

- Training time reduction: 92% average (e.g., 70.5 hrs → 5.31 hrs)
- CTR prediction performance maintained
- Tested trên 3 public datasets

## 4. Hạn chế

- Sliding-window paradigm: O(mn²) complexity scales linearly với sequence length
- DTI ban đầu bị giới hạn small k values
- Bottleneck solutions enable better scalability nhưng phức tạp
