# Review Paper: CETNet: A Collaborative Ensemble Framework for CTR Prediction

**ArXiv ID:** [2411.13700](https://arxiv.org/abs/2411.13700)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết thách thức scaling trong recommendation: chỉ tăng kích thước mô hình đơn lẻ không đảm bảo hiệu suất tốt hơn, ngay cả với dữ liệu dồi dào. Các phương pháp hiện tại thiếu cách tận dụng **sự đa dạng giữa các mô hình khác nhau**. CETNet nhận ra rằng thay vì một mô hình lớn duy nhất, một nhóm các mô hình nhỏ hơn nhưng khác biệt có thể học cộng tác và nắm bắt các interaction patterns khác nhau hiệu quả hơn.

## 2. Phương pháp sử dụng

**CETNet (Collaborative Ensemble Training Network):**

- Triển khai **nhiều mô hình riêng biệt**, mỗi mô hình có **embedding tables riêng** để nắm bắt các feature interaction patterns khác nhau
- **Collaborative learning**: Các mô hình liên tục tinh chỉnh dự đoán lẫn nhau qua feedback iterative — không phải teacher-student mà peer-to-peer
- **Confidence-based fusion**: Sử dụng softmax với **negation entropy** để tính confidence mỗi mô hình → dynamic weighting contributions. Mô hình confident hơn (low entropy) được trọng số cao hơn
- Khuyến khích mô hình học complementary patterns thay vì duplicate nhau

## 3. Thành tựu đạt được

- Vượt trội trên **5 datasets**: AmazonElectronics, TaobaoAds, KuaiVideo + Meta industrial dataset + Criteo/Avazu
- Hiệu suất tương đương/vượt trội với **embedding dimensions nhỏ hơn** — evidence của ensemble efficiency
- Entropy-based weighting cân bằng động contributions hiệu quả
- Xác thực từ Meta industrial-scale dataset

## 4. Hạn chế

- Complexity cao: quản lý nhiều mô hình + interactions giữa chúng khó triển khai production
- Memory cost tăng đáng kể do duy trì embedding tables riêng cho từng mô hình
- Overhead collaborative learning (gradient, backprop qua nhiều models) chưa được phân tích chi tiết
- Không rõ hướng dẫn chọn số lượng mô hình trong ensemble để balance hiệu suất/chi phí
