# Overview: FinalMLP: An Enhanced Two-Stream MLP Model for CTR Prediction

**ArXiv ID:** [2304.00902](https://arxiv.org/abs/2304.00902)
**Venue:** AAAI 2023
**Năm:** 2023
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

- Conventional wisdom: vanilla MLPs không hiệu quả vì khó học multiplicative feature interactions (ví dụ: gender × product_category)
- Paper phát hiện: well-tuned two-stream MLP có thể match hoặc vượt sophisticated models như DeepFM, DCN, xDeepFM
- Occam's razor: nếu simple model đạt hiệu suất tốt, không cần phức tạp — simpler model dễ optimize, faster inference hơn
- Không ai systematically study cách tối ưu two-stream MLP architecture cho CTR — gap nghiên cứu rõ ràng
- Thiếu diversity giữa các streams là bottleneck chính của two-stream MLPs trước đây

## 2. Phương pháp sử dụng

- **Feature Selection Module:** Learnable feature weights riêng cho mỗi stream: x_stream1 = W_1 ⊙ x, x_stream2 = W_2 ⊙ x → tạo diverse representations từ cùng input
- **Stream-wise MLP:** Mỗi stream là standard MLP (multiple hidden layers), có thể asymmetric depths/widths, dùng ReLU/GELU + batch normalization
- **Group-wise Bilinear Fusion:** Capture multiplicative interactions giữa hai streams: interaction = W * (y_stream1 ⊗ y_stream2), group-wise để reduce parameters
- Prediction: pred = sigmoid(concat(y_stream1, y_stream2, interaction) → FC layer)
- End-to-end training với standard BCE loss, Adam optimizer
- Lý do hiệu quả: MLP tự học implicit interactions, bilinear capture explicit multiplicative, two-stream + selection tạo diversity cần thiết

## 3. Thành tựu đạt được

- AUC trên Avazu: 0.7815 (+0.0112 so với DCNv2), MovieLens: 0.9625, Frappe: 0.9820
- A/B test production tại Alibaba: +0.12% CTR — significant ở scale hàng tỷ requests
- Outperforms DCNv2, xDeepFM, AutoInt+, DeepFM một cách nhất quán trên 4 datasets
- Faster training so với các model có complex interaction operations — phù hợp production
- Code open-source, được chấp nhận tại AAAI 2023
- Tác giả: Alibaba & Zhejiang University — đảm bảo cả học thuật và thực tiễn

## 4. Hạn chế

- Feature selection weights W_1, W_2 có thể converge to suboptimal solutions nếu initialization không tốt
- Group-wise bilinear có hyperparameter (group size) cần tune thêm
- MLP có thể chậm hơn specialized networks khi feature space cực lớn (100K+ sparse features)
- Chỉ tested trên 4 datasets + single company A/B test — generalization sang các domains khác chưa rõ
- Simplicity có thể là hạn chế trong scenarios cần many-stream hoặc hierarchical feature processing
