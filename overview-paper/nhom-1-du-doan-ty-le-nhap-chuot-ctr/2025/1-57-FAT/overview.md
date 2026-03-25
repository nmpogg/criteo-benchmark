# Review Paper: FAT: From Scaling to Structured Expressivity - Rethinking Transformers for CTR Prediction

**ArXiv ID:** [2511.12081](https://arxiv.org/abs/2511.12081)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải thích tại sao deep models cho CTR prediction thất bại ở scaling:
- Mismatch cấu trúc: transformers giả định sequential compositionality nhưng CTR data cần combinatorial reasoning
- Trên high-cardinality semantic fields

## 2. Phương pháp sử dụng

- Field-Aware Transformer (FAT): Tích hợp field-based interaction priors vào attention mechanisms
- Decomposed content alignment
- Cross-field modulation
- Complexity scales với số fields, không total vocabulary

## 3. Thành tựu đạt được

- +0.51% AUC improvement trên state-of-the-art methods
- Power-law scaling trong AUC khi model width tăng
- Production: +2.33% CTR, +0.66% RPM
- Scaling law đầu tiên cho CTR models dùng Rademacher complexity

## 4. Hạn chế

- Specific cho CTR prediction domain
- Có thể không generalize sang recommendation scenarios khác
- Limitations chi tiết không được thảo luận
