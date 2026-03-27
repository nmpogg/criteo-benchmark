# Review Paper: MLoRA: Multi-Domain Low-Rank Adaptive Network for CTR Prediction

**ArXiv ID:** [2408.08913](https://arxiv.org/abs/2408.08913)
**Năm:** 2024 | **Venue:** RecSys 2024 | **Deployed:** Alibaba
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết thách thức CTR prediction trong **multi-domain scenarios** — các nền tảng phục vụ users trên nhiều domains (electronics, fashion, food) gặp **data sparsity và disparate data distributions** giữa domains. Các phương pháp hiện tại thêm domain-specific modules riêng cho từng domain → **parameter inflation** nghiêm trọng và training không đủ cho domains nhỏ. Cần giải pháp hiệu quả hơn để adaptation không tốn quá nhiều parameters.

## 2. Phương pháp sử dụng

**MLoRA (Multi-domain Low-Rank Adaptive Network):**

- Triển khai **specialized LoRA module cho mỗi domain** — Low-Rank Adaptation chỉ thêm số lượng nhỏ low-rank parameters cho mỗi domain
- **Giữ core model chung** (shared backbone) — LoRA modules chỉ thêm lightweight domain-specific adjustments
- **Giảm parameter growth** trong khi vẫn cho phép model thích nghi với distribution riêng từng domain
- Áp dụng được với **các deep-learning models khác nhau** — tính linh hoạt cao
- Cân bằng tốt giữa domain-specific performance và parameter efficiency

## 3. Thành tựu đạt được

- Cải thiện đáng kể so với **SOTA baselines** trên nhiều multi-domain datasets
- **Online A/B testing tại Alibaba** cho thấy vượt trội trong production
- Chấp nhận tại **RecSys 2024** — venue hàng đầu recommendation research
- Code công khai cho reproducibility
- Chứng minh giá trị thương mại thực tế tại one of the largest e-commerce platforms

## 4. Hạn chế

- Số liệu improvement cụ thể trên từng domain không được nêu rõ
- Giả định domains có thể xác định rõ ràng — không rõ với blurred domain boundaries
- LoRA rank cho mỗi domain cần tuning, ảnh hưởng performance
- Concept drift (domain distributions thay đổi theo thời gian) chưa thảo luận
- Cold-start problem cho domains hoàn toàn mới chưa giải quyết
