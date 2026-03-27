# Overview: Reformulating CTR Prediction: Learning Invariant Feature Interactions for Recommendation

**ArXiv ID:** [2304.13643](https://arxiv.org/abs/2304.13643)
**Venue:** SIGIR 2023
**Năm:** 2023
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

- Mô hình CTR dùng ERM (Empirical Risk Minimization) học interactions từ lịch sử nhưng generalize kém cho future data do concept drift
- Dữ liệu lịch sử chứa concept drift — xu hướng, mùa vụ, thói quen user thay đổi; ERM bị "lừa" bởi spurious correlations
- IRM (Invariant Risk Minimization) không áp dụng trực tiếp cho CTR vì click data chứa cả invariant và environment-specific correlations
- Giải pháp tiềm năng: chia dữ liệu theo thời gian thành "environments", học interactions ổn định qua các time periods
- Đây là paper đầu tiên áp dụng causal invariance learning vào CTR prediction — gap lớn trong literature

## 2. Phương pháp sử dụng

- **Disentangled Invariant Learning (DIL):** Tách embedding thành e_inv (invariant) + e_env (environment-specific): e_f = e_f^inv + e_f^env
- Chỉ dùng e_inv để học feature interactions — phần ổn định qua thời gian; e_env capture biến động tạm thời
- Loss: L = L_pred(ŷ) + λ × L_inv + μ × L_disentangle (multi-term regularization để tách gỡ inv/env)
- **LightDIL:** Disentanglement ở field level thay vì individual embedding dimension → giảm parameters từ O(k×d) xuống O(f×d)
- Multi-environment training: chia dữ liệu lịch sử thành m environments (time windows), tối ưu đồng thời
- Penalty đảm bảo e_inv và e_env orthogonal; dự đoán robust across environments
- Áp dụng được trên top của FM, AFM, và các FM-based models

## 3. Thành tựu đạt được

- LightDIL vượt trội tất cả baselines (FM, FwFMs, AFM, AutoFIS, PROFIT) trên ML-10M & Douban datasets
- AUC cao hơn trên future data (out-of-time test set) — chứng minh generalization qua temporal shift
- Statistical significance: p-value < 0.05 cho tất cả improvements
- Là paper đầu tiên áp dụng causal invariance learning vào CTR prediction — contribution học thuật quan trọng
- Chấp nhận tại SIGIR 2023 (top-tier IR/RecSys conference)
- Code: https://github.com/zyang1580/DIL

## 4. Hạn chế

- Cách chia "environments" là tuỳ ý — nếu chia không hợp lý thì invariant learning không hiệu quả
- Không có hướng dẫn lý thuyết chọn số lượng environments và độ dài mỗi time period
- DIL full version gặp scaling issues nếu số features lớn (mỗi feature cần 2 embedding vectors)
- Giả sử dữ liệu stationary trong mỗi environment; sudden distribution shift quá lớn → không hoạt động tốt
- Chỉ 2 datasets; cần tuning cả λ và μ; không có metric chuẩn đánh giá chất lượng disentanglement
