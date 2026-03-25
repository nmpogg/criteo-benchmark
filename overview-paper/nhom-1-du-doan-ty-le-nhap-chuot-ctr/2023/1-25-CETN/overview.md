# Overview: CETN: Contrast-enhanced Through Network for CTR Prediction

**ArXiv ID:** [2312.09715](https://arxiv.org/abs/2312.09715)
**Venue:** TOIS 2024
**Năm:** 2023
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

- Parallel-structure CTR models (DCN, FinalMLP, xDeepFM) có subcomponents operate independently — thiếu supervisory signals từ nhau
- Features interact trong nhiều semantic spaces cùng lúc (product-category space, user-demographic space, temporal space) nhưng models xử lý đơn không gian
- Contrastive learning rất thành công ở computer vision và NLP nhưng chưa được khai thác tốt cho CTR prediction
- Serial models (DeepFM) combine features sequentially — không capture multi-view representations đồng thời
- Cần một framework kết hợp được multi-space interactions với self-supervised signals từ data augmentation

## 2. Phương pháp sử dụng

- **Semantic Space Segmentation:** Product-based feature interactions phân chia data vào các different semantic spaces khác nhau
- **Distinct Activation Functions:** Mỗi semantic space có riêng activation (ReLU, Sigmoid, Tanh, ELU, ...) → tăng diversity của representations
- **Data Augmentation via Perturbation:** Feature dropout, Gaussian noise, mixup-style augmentation; original + augmented views đều feed vào các spaces
- **Self-Supervised Signals:** Mỗi space được training với auxiliary loss: proximity loss giữa original và augmented predictions (KL divergence hoặc cosine similarity)
- **Through Connections:** Attention-based routing giữa các spaces: output_i = f(output_i, attention(output_j)) — cho phép information flow cross-space
- Joint multi-task loss: L_total = L_main + λ₁·L_self1 + λ₂·L_self2 + ... (cân bằng main task và auxiliary signals)

## 3. Thành tựu đạt được

- Outperforming 20 baseline models trên 4 real-world datasets — comprehensive comparison
- AUC improvement: +0.3–0.8% so với best baseline; Logloss: -0.005 đến -0.015
- Consistent #1 hoặc top-2 trên tất cả datasets
- Ablation studies chứng minh mỗi component (segmentation, augmentation, self-supervised) đều đóng góp
- Chấp nhận tại TOIS 2024 (ACM Transactions on Information Systems — journal A*)
- Code: https://github.com/salmon1802/CETN

## 4. Hạn chế

- Semantic space definition via product-based interactions là heuristic — không có systematic way chọn số spaces
- Augmentation strategy (dropout, noise, mixup) được thiết kế ban đầu cho vision domain — không rõ optimal cho CTR
- Mỗi space dùng activation khác nhau thêm hyperparameter choices, và sensitivity analysis chưa rõ ràng
- Complexity cao: multiple spaces + activations + self-supervised losses = nhiều hyperparameters cần tune (λ values)
- Không có production A/B test; không phân tích extreme cases (cold-start); statistical significance của improvements chưa được kiểm tra
