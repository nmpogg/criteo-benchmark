# Review Paper: MLoRA: Multi-Domain Low-Rank Adaptive Network for CTR Prediction

**ArXiv ID:** [2408.08913](https://arxiv.org/abs/2408.08913)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

CTR prediction trong multi-domain scenarios:
- Data sparsity & differing data distributions giữa các domain

## 2. Phương pháp sử dụng

- Specialized LoRA module cho mỗi domain → domain-specific adaptation
- Parameter efficiency
- Áp dụng cho various deep-learning models

## 3. Thành tựu đạt được

- Hiệu suất cải thiện đáng kể so với SOTA baselines
- Deployed thành công tại Alibaba với positive A/B testing
- Code công khai cho reproducibility

## 4. Hạn chế

- Overhead storage cho mỗi LoRA module
- Không thảo luận cold-start problem cho domains mới
- LoRA technique có thể không optimal cho tất cả domains
