# Review Paper: SGCTR: Infer As You Train - A Symmetric Paradigm of Masked Generative for CTR Prediction

**ArXiv ID:** [2511.14403](https://arxiv.org/abs/2511.14403)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết bất cân xứng trong generative models cho CTR:
- Hiện tại chỉ dùng generative techniques trong training, revert sang discriminative methods ở inference
- Mất mát khả năng generative khi dự đoán

## 2. Phương pháp sử dụng

- SGCTR: masked generative modeling áp dụng symmetric trên cả training & inference phases
- Inference stage: iteratively refine input features dùng learned generative capabilities
- Dùng generative capabilities cho prediction thay vì chỉ binary classification

## 3. Thành tựu đạt được

- Applying generative paradigm symmetrically unlock power trong CTR prediction
- Giảm noise trong features, cải thiện độ chính xác
- Paradigm mới cho CTR prediction

## 4. Hạn chế

- Bài báo ngắn (4 pages), recently submitted (Nov 2025)
- Thiếu comprehensive analysis về computational costs
- Hạn chế ablation studies chi tiết
- Scalability considerations chưa rõ
