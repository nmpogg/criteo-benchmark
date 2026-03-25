# Review Paper: GAP-Net: Calibrating User Intent via Gated Adaptive Progressive Learning for CTR Prediction

**ArXiv ID:** [2601.07613](https://arxiv.org/abs/2601.07613)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết ba thách thức trong sequential user behavior modeling cho CTR prediction:
- Attention Sink: Models tập trung probability mass vào noisy behaviors
- Static Query Assumption: Bỏ qua dynamic intent shifts
- Rigid View Aggregation: Không thích ứng weighted temporal signals

## 2. Phương pháp sử dụng

Triple Gating Architecture - progressively refines information qua feature levels:
- Adaptive Sparse-Gated Attention (ASGA): Enforces sparsity ở micro-level để suppress noise
- Gated Cascading Query Calibration (GCQC): Dynamically aligns user intent bằng connecting real-time triggers với long-term memories
- Context-Gated Denoising Fusion (CGDF): Macro-level modulation cho multi-view sequence aggregation
- Hierarchical gating mechanisms từ micro → meso → macro level

## 3. Thành tựu đạt được

- Substantial improvements trên state-of-the-art baselines
- Superior robustness chống lại interaction noise và intent drift
- Extensive experiments trên industrial datasets

## 4. Hạn chế

- Không cụ thể hóa các improvement metrics (AUC, precision, etc.)
- Độ phức tạp của triple gating architecture có thể ảnh hưởng đến inference latency
- Chưa có online A/B testing results
