# Review Paper: SUAN: Exploring Scaling Laws of CTR Model for Online Performance Improvement

**ArXiv ID:** [2508.15326](https://arxiv.org/abs/2508.15326)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Khám phá scaling laws trong mô hình CTR prediction (tương tự như trong LLMs):
- Cân bằng độ chính xác với ràng buộc deployment thực tiễn

## 2. Phương pháp sử dụng

- SUAN (Stacked Unified Attention Network) với UAB làm behavior sequence encoders
- Knowledge distillation từ SUAN high-grade sang LightSUAN (lightweight)
- Sparse self-attention và parallel inference strategies
- Online distillation training

## 3. Thành tựu đạt được

- LightSUAN triển khai online: CTR +2.81%, CPM +1.69%
- Chứng minh scaling laws trên 3 order magnitude
- Distilled lightweight version vượt performance baseline

## 4. Hạn chế

- Tradeoff giữa inference time
- Cần knowledge distillation để đạt deployment feasibility
- Các hạn chế cụ thể không được chi tiết
