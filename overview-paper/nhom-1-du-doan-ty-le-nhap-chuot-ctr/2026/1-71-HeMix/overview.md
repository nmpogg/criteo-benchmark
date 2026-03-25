# Review Paper: HeMix: Query-Mixed Interest Extraction and Heterogeneous Interaction: A Scalable CTR Model for Industrial Recommender Systems

**ArXiv ID:** [2602.09387](https://arxiv.org/abs/2602.09387)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết thách thức learning effective feature interactions trong industrial recommendation systems:
- Xử lý sparse multi-field data và exceptionally long user behavior sequences
- Tối ưu scaling efficiency cho production systems

## 2. Phương pháp sử dụng

HeMix Model với hai thành phần chính:
- Query-Mixed Interest Extraction Module: Capture user preferences đồng thời qua dynamic & fixed query mechanisms, xử lý historical + immediate behavioral data
- HeteroMixer Block: Thay thế traditional self-attention bằng structure có multi-head token fusion, heterogeneous interaction & group-aligned reconstruction pipelines
- Thiết kế efficient cross-feature analysis

## 3. Thành tựu đạt được

- Scaling efficiency: tăng parameters → consistent accuracy improvements
- Triển khai production thực tế trên AMAP platform:
  - +3.61% GMV improvement
  - +2.78% PV_CTR gain
  - +2.12% UV_CVR increase
- Outperform DLRM baseline trên multiple metrics

## 4. Hạn chế

- Complexity cao của HeteroMixer block - khó maintain & debug
- Trade-off giữa model capacity & inference latency chưa rõ ràng
- Evaluation chủ yếu trên AMAP - generalization cần xác minh
- Long sequence processing vẫn có memory constraints
