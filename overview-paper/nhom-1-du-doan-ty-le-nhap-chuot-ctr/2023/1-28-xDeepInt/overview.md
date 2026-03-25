# Overview: xDeepInt: a hybrid architecture for modeling vector-wise and bit-wise feature interactions

**ArXiv ID:** [2301.01089](https://arxiv.org/abs/2301.01089)
**Venue:** arXiv 2023
**Năm:** 2023
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

- Hai loại feature interactions tồn tại đồng thời: vector-wise (giữa embedding vectors nguyên vẹn) và bit-wise (mức từng dimension trong embeddings)
- DeepFM, xDeepFM chủ yếu focus vào vector-wise; DCN, AutoInt xử lý high-order nhưng không handle cả hai loại cùng lúc
- Dữ liệu CTR có tương tác ở cả mức vector (macro: feature-field level) và mức bit (micro: embedding dimension level) với priorities khác nhau
- Subspace structure trong embeddings có thể encode different semantic aspects — không ai khai thác cho CTR
- Gap: không có phương pháp cho phép balanced mixing cả hai loại interactions ở các orders khác nhau

## 2. Phương pháp sử dụng

- **Polynomial Interaction Network (PIN):** Học higher-order vector-wise interactions đệ quy với residual connections: z^(l+1) = z^(l) + φ(W^(l) ⊗ z^(l))
- Linear activation (φ = identity) cho best performance trong PIN; residual connections tránh vanishing gradients
- **Subspace-Crossing Mechanism:** Chia embedding space thành h subspaces (dimension k'=k/h), crossing giữa subspaces capture bit-wise interactions
- Complexity: h² × F² parameters mỗi PIN layer (h subspaces, F fields) — controllable
- Combined feature selection + interaction selection dùng L1 regularization/gating để prune redundant interactions
- Architecture tổng thể: embedding layer → l PIN layers với subspace-crossing → FC layers → prediction
- Typical config: h=4 subspaces, F=30 fields, l=3 layers → ~1.4M parameters cho interaction part

## 3. Thành tựu đạt được

- Best AUC trên Avazu, Criteo, Taobao so với DeepFM, xDeepFM, AutoInt, DCN-v2
- Cải thiện AUC: ~0.5–1.5% — significant trong CTR domain (mỗi 0.1% AUC là đáng kể ở scale lớn)
- Ablation: PIN alone tốt, subspace-crossing alone tốt hơn baselines, kết hợp cả hai = best performance
- Linear activation > ReLU > Sigmoid; 3–4 layers optimal cho cả performance và efficiency
- Feature/interaction selection cải thiện thêm ~0.3–0.5% AUC, giảm ~20–30% parameters
- TensorFlow open-source implementation

## 4. Hạn chế

- Nhiều hyperparameters cần tune: h (subspaces), k' (subspace dim), l (layers), α (regularization) — tuning tốn kém
- "Bit-wise interactions" có thực sự tồn tại vật lý hay chỉ là construct toán học? Interpretability hạn chế
- Không có hướng dẫn rõ khi nào ưu tiên vector-wise vs bit-wise interactions cho dataset cụ thể
- Chưa test trên datasets khổng lồ (Terabyte-scale); baselines xDeepFM, DeepFM từ 2018–2019 đã cũ
- Integration vào production system phức tạp; không có chứng minh lý thuyết rằng hybrid approach là tối ưu
