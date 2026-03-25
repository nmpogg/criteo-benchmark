# Review Paper: MDL — A Unified Multi-Distribution Learner in Large-scale Industrial Recommendation through Tokenization

**ArXiv:** [2602.07520](https://arxiv.org/abs/2602.07520) | **Năm:** 2026
**Tác giả:** Shanlei Mu, Yuchen Jiang, Shikang Wu, Shiyong Hong, Tianmu Sha, Junjie Zhang, Jie Zhu, Zhe Chen, Zhe Wang, Jingjian Lin

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **multi-scenario & multi-task learning** cho hệ thống recommendation quy mô lớn, giải quyết các vấn đề khi cùng một mô hình phải phục vụ nhiều kịch bản (scenarios) và nhiều mục tiêu (tasks) đồng thời:

- **Underutilization of parameters:** Mô hình lớn có hàng triệu/tỷ parameters nhưng chỉ một phần nhỏ được activate cho mỗi scenario/task cụ thể. Ví dụ: parameters học cho "Douyin Search" hầu như không được dùng khi serving "Douyin Feed" → lãng phí capacity.
- **Khó jointly model scenario + task:** Scenarios (search, feed, live) và tasks (CTR, conversion rate, watch time) có characteristics rất khác nhau. Mô hình truyền thống hoặc dùng shared-bottom (mất task-specific info) hoặc hoàn toàn tách biệt (mất cross-scenario knowledge).
- **Distribution prediction đa dạng:** Mỗi scenario + task tạo ra một output distribution khác nhau → cần cơ chế dự đoán multi-distribution hiệu quả.

**Ý tưởng chính:** Lấy cảm hứng từ language models — biến scenarios và tasks thành **tokens** trong cùng vocabulary với features, cho phép xử lý thống nhất qua attention mechanisms.

## 2. Phương pháp sử dụng

**MDL Framework — Information Tokenization** gồm 3 cơ chế tương tác:

**1. Feature Token Self-Attention:**
- Biến mỗi feature field thành token, áp dụng self-attention để capture **feature-feature interactions**
- Giống cách Transformer xử lý word tokens, MDL xử lý feature tokens
- Cho phép rich feature interaction learning

**2. Domain-Feature Attention:**
- "Domain" = combination (scenario, task) — ví dụ (Search, CTR) hoặc (Feed, Watch_Time)
- Domain token attend vào feature tokens → **adaptive feature activation** tùy theo domain
- Cùng feature "user_age", domain (Search, CTR) có thể dùng khác so với domain (Feed, Watch_Time)
- Giải quyết vấn đề parameter utilization: features được activate khác nhau cho mỗi domain

**3. Domain-Fused Aggregation:**
- Tổng hợp outputs từ multiple domains để tạo **unified distribution prediction**
- Cross-domain knowledge sharing: kiến thức từ domain (Search, CTR) hỗ trợ domain (Search, Conversion)
- Stacking 3 cơ chế theo layers: bottom-up, layer-wise activation

**Triết lý:** Scenario và task information "prompt" mô hình (tương tự prompt engineering) để activate đúng phần parameters cần thiết.

## 3. Thành tựu đạt được

- **Triển khai production trên Douyin Search** (TikTok Search) phục vụ hàng trăm triệu users mỗi ngày
- **Online testing 1 tháng:**
  - **+0.0626% LT30** improvement (long-term user satisfaction metric)
  - **-0.3267% change query rate** reduction (users ít phải thay đổi query → search chính xác hơn)
  - Trong production Douyin scale, 0.06% improvement ảnh hưởng hàng triệu users
- **Effective parameter utilization:** Chứng minh tokenization approach sử dụng parameters hiệu quả hơn shared-bottom hay tower-based architectures
- **Vượt trội so với multi-scenario/multi-task baselines** hiện có trên industrial datasets

## 4. Hạn chế

- **Token overhead:** Tokenization thêm processing steps, có thể tăng inference latency
- **Hyperparameter complexity:** 3 cơ chế tương tác × nhiều layers → nhiều hyperparameters cần tune
- **Domain-specific metrics:** LT30 và change query rate là metrics đặc thù Douyin Search, khó so sánh trực tiếp với standard AUC/LogLoss trên public datasets
- **Scaling to many domains:** Khi số scenarios × tasks rất lớn (>20 domains), token vocabulary và attention costs tăng
- **Chưa có public benchmark results** — chỉ đánh giá trên proprietary Douyin datasets
