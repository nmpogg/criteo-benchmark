# Review Paper: SSEDS: Single-Shot Embedding Dimension Search in Recommender System

**ArXiv ID:** [2204.03281](https://arxiv.org/abs/2204.03281)
**Năm:** 2022
**Tác giả:** Tencent (WeChat team)
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Hiện tại, hầu hết CTR models dùng **uniform embedding dimension** cho tất cả feature fields — gây lãng phí cho fields đơn giản và thiếu capacity cho fields phức tạp. Tìm optimal mixed-dimensional embeddings là bài toán **NP-hard combinatorial**. Các phương pháp NAS truyền thống tốn kém (vài ngày đến vài tuần).

**Motivation:** Cần phương pháp **nhanh, single-shot** để tự động gán embedding dimension tối ưu cho từng feature field, giảm parameters mà vẫn giữ accuracy, áp dụng được trên production.

## 2. Phương pháp sử dụng

**Single-Shot Embedding Dimension Search (SSEDS):**

1. **Dimension Importance Scoring:** Tính "importance" của từng embedding dimension cho mỗi feature field — dựa trên gradient magnitude và feature contribution analysis
2. **Single-Shot Pruning:** Rank dimensions theo importance → loại bỏ dimensions có importance thấp nhất theo parameter budget constraints — chỉ 1 pass duy nhất, không iterative
3. **Model-Agnostic Design:** Hoạt động với bất kỳ CTR architecture (DeepFM, Wide&Deep, etc.), không phụ thuộc framework cụ thể

**Flow:** Train original model → Tính importance scores → Rank & prune → Fine-tune (optional) → Deploy

## 3. Thành tựu đạt được

| Metric | Kết quả |
|--------|---------|
| **Parameter reduction** | 90% giảm parameters mà giữ accuracy |
| **Compatibility** | Model-agnostic, hoạt động trên nhiều architectures |
| **Training efficiency** | Nhanh hơn đáng kể so với NAS approaches |
| **Production** | Deployed trên WeChat Subscription platform |
| **A/B Testing** | 7-day A/B test — cải thiện đáng kể recommendation performance |

Datasets đánh giá: Criteo, Avazu.

## 4. Hạn chế

- **Heuristic scoring:** Importance scoring dựa trên gradient có thể không capture toàn bộ feature importance
- **Single-shot limitation:** Một pass pruning có thể miss interactions giữa các pruned dimensions — không có cơ hội điều chỉnh
- **Fine-tuning chưa rõ:** Post-pruning fine-tuning strategy không được định nghĩa rõ ràng
- **Thiếu lý thuyết:** Không có proof về tính optimal của pruning strategy
- **Scope hẹp:** Chỉ tối ưu embedding dimensions, không tối ưu feature engineering hay model architecture
- **Limited datasets:** Chỉ đánh giá trên 2 public datasets (Criteo, Avazu), chưa rõ generalizability
