# Overview: EulerNet: Adaptive Feature Interaction Learning via Euler's Formula for CTR Prediction

**ArXiv ID:** [2304.10711](https://arxiv.org/abs/2304.10711)
**Venue:** SIGIR 2023
**Năm:** 2023
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

- High-order feature interactions (k≥3) crucial cho CTR nhưng tính toán exponentially expensive (100K features, k=3 → hàng triệu tổ hợp)
- Hầu hết methods phải manually design maximal order (max order=3) → mất potential high-order patterns ở các order cao hơn
- Filter out "useless" interactions nhưng không biết interactions nào thực sự useless → suboptimal pruning
- Toán học số phức (complex numbers) có tính chất đặc biệt cho polynomial operations — chưa ai leverage cho CTR
- Gap: không có phương pháp nào sử dụng complex number mathematics để giải quyết feature interaction problem

## 2. Phương pháp sử dụng

- **Core: Euler's Formula trong Feature Space:** e^(iθ) = cos(θ) + i·sin(θ)
- Biểu diễn feature interactions trong complex vector space: mỗi feature → (modulus r, phase θ)
- High-order computation: (re^(iθ))^k = r^k · e^(ikθ) → exponential power trở thành linear phase shift
- k-th order interaction: z^(k) = (r₁·r₂·...·rₙ)^(1/k) · e^(i(θ₁+θ₂+...+θₙ)) — giảm từ exponential xuống O(d) parameters
- Unified implicit (standard MLP) + explicit (Euler layer) integration via attention/weighted sum
- Network tự học optimal (r, θ) cho mỗi feature, không cần pre-specify interaction order

## 3. Thành tựu đạt được

- Criteo AUC: 0.8111 (+0.0049 so với xDeepFM), Avazu: 0.7842, MovieLens: 0.9627
- Consistent top rank trên tất cả 3 benchmarks so với 10+ baseline models
- Model parameters comparable với DCN nhưng handles significantly higher effective interaction orders
- Được tích hợp vào RecBole library — major recommender systems library được cộng đồng sử dụng rộng
- Chấp nhận tại SIGIR 2023 (top-tier IR conference)
- Code: https://github.com/RUCAIBox/EulerNet

## 4. Hạn chế

- Complex space mapping (r, θ) khó interpret về mặt vật lý — phase θ có ý nghĩa gì với feature thực tế?
- Geometric mean (r₁·r₂·...·rₙ)^(1/k) gây magnitude collapse nếu bất kỳ r_i nào nhỏ
- Exponential operations e^(ikθ) có thể numerical unstable với large k hoặc θ lớn
- Improvements relatively modest (0.18–0.49% AUC) — chưa rõ statistical significance
- Integration với existing CTR systems phức tạp vì uncommon feature space representation (complex numbers)
