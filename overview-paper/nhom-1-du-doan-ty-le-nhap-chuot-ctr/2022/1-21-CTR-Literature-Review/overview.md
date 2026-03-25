# CTR Prediction in Online Advertising: A Literature Review

**ArXiv:** [2202.10462](https://arxiv.org/abs/2202.10462)
**Năm:** 2022 | **Venue:** Information Processing & Management, 59(2): 102853
**Tác giả:** Yanwu Yang, Panyu Zhai
**Nhóm:** 1 — Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

**Khảo sát toàn diện (85 trang)** về lĩnh vực CTR prediction trong quảng cáo trực tuyến. Paper nhận thấy thiếu một survey hệ thống bao quát từ mô hình truyền thống đến deep learning, nên thực hiện:

- Hệ thống hóa và phân loại **tất cả frameworks modeling** chính cho CTR prediction
- Phân tích ưu/nhược điểm và đánh giá hiệu suất của từng nhóm mô hình
- Xác định **xu hướng nghiên cứu hiện tại, thách thức chính, và hướng đi tương lai**

**Đối tượng hướng đến:** Nhà nghiên cứu Information Systems, marketing scholars, và những người mới bước vào lĩnh vực CTR prediction.

---

## 2. Phương pháp sử dụng

### Systematic Literature Review

#### Phân loại 4 nhóm mô hình chính:

1. **Multivariate Statistical Models:** Logistic Regression (LR), Bayesian models — đơn giản, interpretable, nhưng chỉ capture linear relationships
2. **Factorization Machines (FM) based Models:** FM, FFM, AFM — model pairwise feature interactions, khắc phục data sparsity tốt hơn LR
3. **Deep Learning Models:** Wide&Deep, DeepFM, DCN, xDeepFM, AutoInt — học high-order feature interactions tự động, hiệu suất cao nhất
4. **Tree Models:** GBDT, XGBoost — xử lý tốt non-linear relationships, thường dùng kết hợp với DL models

#### Phân loại theo Feature Interaction:

- **Explicit vs Implicit:** Explicit (FM, DCN cross network) tính interaction trực tiếp; Implicit (DNN) học ngầm qua hidden layers
- **Low-order vs High-order:** 2nd-order (FM), arbitrary-order (DCN, xDeepFM, AutoInt)
- **Bit-wise vs Vector-wise:** Tương tác ở mức từng bit trong embedding hay ở mức vector

#### So sánh hiệu suất

- Tổng hợp kết quả benchmark trên các datasets phổ biến (Criteo, Avazu, KDD Cup...)
- So sánh đa chiều: accuracy, computational cost, interpretability, scalability

---

## 3. Thành tựu đạt được

### Đóng góp chính

- **Taxonomy toàn diện nhất** tính đến 2022: phân loại rõ ràng 4 nhóm modeling + phân loại feature interaction types
- **85 trang, 12 hình, 9 bảng:** Chi tiết frameworks, advantages/disadvantages, implementations
- **Timeline evolution:** Vẽ rõ quá trình phát triển LR → FM → DNN → Hybrid models, giúp hiểu logic phát triển
- **Benchmark synthesis:** Tổng hợp performance comparison qua nhiều papers, tạo reference point thống nhất
- **Roadmap nghiên cứu:** Xác định rõ challenges và future directions, hữu ích cho researchers mới

### Giá trị thực tiễn

- Là **entry point hiệu quả** cho người mới: đọc 1 paper nắm được toàn cảnh lĩnh vực
- Phân tích ưu/nhược giúp practitioners chọn model phù hợp cho use case cụ thể
- Xuất bản trên IP&M (IF cao), khẳng định chất lượng survey

---

## 4. Hạn chế

- **Breadth vs Depth trade-off:** Do bao quát rộng (4 nhóm model, hàng chục papers), độ sâu kỹ thuật cho từng mô hình bị hạn chế — không đi sâu vào mathematical formulation hay implementation tricks
- **Thiếu thảo luận về triển khai production:** Tập trung vào offline modeling, ít đề cập challenges khi deploy real-time CTR systems (latency, serving infrastructure, A/B testing methodology)
- **Cutoff point 2022:** Bỏ lỡ các xu hướng mới sau 2022: LLM-enhanced CTR, generative CTR, scaling laws, MoE architectures, knowledge distillation frameworks
- **Thiếu practical guidelines:** Không đưa ra khuyến nghị cụ thể "nên dùng model nào cho scenario nào" — chủ yếu liệt kê và phân loại
- **Dataset bias:** Hầu hết papers được survey đều benchmark trên Criteo/Avazu — thiếu phân tích về domain-specific datasets (e-commerce, video, social media)
- **Chưa cover multi-task learning:** CTR prediction trong production thường kết hợp với CVR, engagement prediction — survey chưa phân tích hướng multi-task/multi-objective
