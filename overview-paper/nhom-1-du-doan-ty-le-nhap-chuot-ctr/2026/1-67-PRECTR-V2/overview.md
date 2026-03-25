# Review Paper: PRECTR-V2: Unified Relevance-CTR Framework with Cross-User Preference Mining, Exposure Bias Correction, and LLM-Distilled Encoder Optimization

**ArXiv ID:** [2602.20676](https://arxiv.org/abs/2602.20676)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Phát triển PRECTR với focus trên coordinating search relevance matching và CTR prediction:
- Sparse behavioral data cho low-activity users
- Distribution mismatch giữa training và ranking data (exposure bias)
- Architectural constraints từ frozen encoders (BERT)

## 2. Phương pháp sử dụng

- Cross-User Preference Mining: Mine global relevance preferences cho specific queries, enable cold-start personalization
- Exposure Bias Correction: Constructing hard negative samples thông qua embedding noise injection và label reconstruction; optimize relative ranking via pairwise loss
- LLM-Distilled Encoder: Pretrain lightweight transformer-based encoder thông qua knowledge distillation từ LLM, replace frozen BERT module
- Joint optimization của representation learning và task-specific fine-tuning

## 3. Thành tựu đạt được

- Vượt qua traditional Emb+MLP paradigm
- Integration thành công của relevance và CTR objectives
- Lightweight encoder thay thế BERT module giảm chi phí inference

## 4. Hạn chế

- Submitted 02/2026 - chưa có kết quả numerical cụ thể trong abstract
- Chưa có kết quả online A/B testing
- Chưa public detailed performance metrics
