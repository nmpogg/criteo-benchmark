# Review Paper: PRECTR: A Synergistic Framework for Integrating Personalized Search Relevance Matching and CTR Prediction

**ArXiv ID:** [2503.18395](https://arxiv.org/abs/2503.18395)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết fundamental challenge: Traditional approach xử lý search relevance matching và CTR prediction như separate tasks:
- Tạo inconsistencies giữa các models
- Relevance models chỉ focus vào objective text matching, bỏ qua personalized user preferences

## 2. Phương pháp sử dụng

- Unified Framework: Integrate CTR prediction và relevance matching into one framework
- Personalization Enhancement: Analyze past users' preferences cho similar queries để incorporate user-specific relevance preferences
- Two-stage training strategy + semantic consistency regularization để prevent recommending irrelevant high-CTR items
- Conditional probability fusion mechanism kết hợp cả hai tasks

## 3. Thành tựu đạt được

- Unified modeling outperforms conventional divide-and-conquer paradigm
- Experiments trên proprietary production datasets
- Online A/B testing chứng minh practical effectiveness

## 4. Hạn chế

- Kết quả chỉ trên proprietary/production datasets (không public)
- Không có benchmark trên standard datasets
- Limited details về specific improvement percentages
