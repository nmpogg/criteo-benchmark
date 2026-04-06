# Review Paper: Wide & Deep Learning for Recommender Systems

**ArXiv ID:** [1606.07792](https://arxiv.org/abs/1606.07792)  
**Năm:** 2016  
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)  
**Tác giả:** Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra et al. (Google Inc.)

---

## 1. Paper này đang nghiên cứu gì?

Bài báo này khám phá bài toán cổ điển trong hệ thống gợi ý: cân bằng giữa **memorization** (ghi nhớ các mẫu tương tác hiệu năng cao) và **generalization** (khái quát hóa để dự đoán các tổ hợp đặc trưng chưa từng thấy). Trong Google Play App Store với hơn 1 tỷ người dùng, các mô hình chỉ dùng một chiến lược thường gặp vấn đề:

- **Mô hình tuyến tính (Wide):** Sử dụng cross-product feature transformations, có khả năng memorization tốt nhưng cần kỹ sư tính toán rất nhiều đặc trưng, không generalize tốt đến dữ liệu chưa thấy.
- **Mạng nơ-ron sâu (Deep):** Học biểu diễn embedding thưa thớt thành vector dày đặc, generalize tốt nhưng có xu hướng **over-generalize** - dự đoán xác suất cao cho các cặp (user, item) mà trong thực tế không có tương tác.

Vấn đề cụ thể: khi ma trận user-item rất thưa và có rank cao (ví dụ: người dùng có sở thích riêng, sản phẩm niche), mạng nơ-ron sâu vẫn cho kết quả dự đoán khác 0, dẫn đến gợi ý không liên quan. Bài báo đề xuất **Wide & Deep Framework** - kết hợp đóng gói cả hai thành phần, huấn luyện chung để tận dụng ưu điểm của memorization (qua wide) và generalization (qua deep).

---

## 2. Phương pháp sử dụng

### Kiến trúc Wide & Deep

**Thành phần Wide (Tuyến tính):**
- Mô hình: y = w^T x + b, với x là vector đặc trưng d chiều
- Sử dụng cross-product transformation: φ_k(x) = ∏(x_i^c_ki), trong đó c_ki ∈ {0,1}
- Ví dụ: AND(user_installed_app=netflix, impression_app=pandora) = 1 nếu điều kiện đúng
- Lợi ích: Memorize các tương tác cụ thể, interpretable, hiệu quả trên dữ liệu thưa

**Thành phần Deep (Mạng nơ-ron):**
- Kiến trúc: feed-forward neural network với multiple hidden layers
- Input: Sparse categorical features (one-hot encoded) → Embedding layer → Dense vectors (32 chiều mỗi feature)
- Hidden layers: 3 lớp ReLU (256, 512, 1024 units) kích hoạt với ReLU
- Tính toán: a^(l+1) = f(W^(l) a^(l) + b^(l)), với f là ReLU
- Lợi ích: Generalize tốt đến unseen feature combinations, học biểu diễn tự động

**Huấn luyện Chung (Joint Training):**
- Kết hợp output: P(Y=1|x) = σ(w_wide^T[x, φ(x)] + w_deep^T a^(l_f) + b)
- Sigmoid σ(·) cho binary classification (CTR prediction)
- Tối ưu hóa: Sử dụng **FTRL (Follow-the-Regularized-Leader)** cho wide component (L1 regularization), **AdaGrad** cho deep component
- Minibach stochastic optimization, backpropagation gradient được propagate đến cả hai phần
- **Sự khác biệt với ensemble:** Ensemble training từng mô hình riêng rẽ, kết hợp dự đoán lúc inference. Joint training tối ưu tất cả tham số cùng lúc, cho phép wide component chỉ cần complement các weakness của deep component.

### Hệ thống Triển khai

**Data Generation:**
- Mỗi impression (lần hiển thị ứng dụng) → 1 training example
- Label: app acquisition (1 = cài đặt, 0 = không)
- Feature normalization: Continuous features mapping sang [0,1] qua CDF, chia thành n_q quantiles
- Vocabulary generation: String features → Integer IDs (chỉ features xuất hiện ≥ threshold lần)

**Model Training:**
- Dữ liệu: >500 tỷ examples từ Google Play
- Model structure: Cross-product transformations (user installed apps × impression apps) cho wide; 32-dimensional embeddings × N fields ≈ 1200-dim concatenated vectors cho deep
- Warm-starting: Khởi tạo embeddings và linear weights từ mô hình trước để tránh retrain từ đầu (tiết kiệm thời gian, accelerate convergence)
- Model verification: Dry run kiểm tra trước khi deploy

**Model Serving:**
- Latency requirement: O(10ms) cho mỗi request
- Optimization: Multithreading, split batch nhỏ (50 items/thread × 4 threads) thay vì single batch (200 items) → 14ms (từ 31ms)

---

## 3. Thành tựu đạt được

### Kết quả Online (A/B Testing, 3 tuần)

| Mô hình | Offline AUC | Online App Acquisition Gain |
|---------|-------------|---------------------------|
| Wide (control) | 0.726 | 0% |
| Deep | 0.722 | +2.9% |
| **Wide & Deep** | **0.728** | **+3.9%** |

- **+3.9% relative improvement** so với wide-only baseline (statistically significant)
- **+1.0% gain** so với deep-only model
- Kết quả đáng chú ý: offline AUC của Wide & Deep chỉ cao hơn wide 0.002 (+0.3%), nhưng online acquisition tăng 3.9% → online exploration & learning from new user responses có giá trị lớn

### Serving Performance

| Batch Size | Threads | Latency (ms) |
|-----------|---------|--------------|
| 200 | 1 | 31 |
| 100 | 2 | 17 |
| 50 | 4 | 14 |

- Multithreading optimization giảm latency từ 31ms → 14ms (bao gồm serving overhead)
- Xử lý >10 triệu apps/giây tại peak traffic
- Thỏa mãn latency requirement O(10ms) cho production

### Đặc điểm Kỹ thuật

- **Model size & complexity:** Joint training cho phép wide component nhỏ gọn (chỉ cần complement deep's weakness) thay vì full-size wide model (trong ensemble); giảm tổng tham số so với ensemble
- **Convergence:** Mạnh mẽ, ổn định qua >500B training examples
- **Generalization:** Cân bằng memorization & generalization hiệu quả → cao hơn pure memorization hoặc pure generalization

---

## 4. Hạn chế

### Kỹ thuật

1. **Feature Engineering Overhead:** Wide component vẫn cần cross-product transformations được thiết kế thủ công (ví dụ: chọn cặp feature nào để tạo interaction). Mặc dù deep component tự động học high-order patterns, việc xác định cross-product transformations hiệu quả vẫn đòi hỏi domain expertise.

2. **Embedding Initialization:** Embeddings khởi tạo ngẫu nhiên, không dùng pre-training (khác với FNN). Không rõ pre-training từ factorization machine có cải thiện không.

3. **Hyperparameter Sensitivity:** Bài báo không chi tiết về sensitivity analysis cho embedding dimension, network depth, regularization strength. Chỉ báo cáo fixed architecture (3 ReLU layers, 32-dim embeddings).

4. **Scalability Concerns:** 
   - Warm-starting mechanism chỉ documented briefly; impact của initialization lên training dynamics chưa phân tích kỹ
   - Vocabulary generation (features xuất hiện ≥ threshold) có thể bỏ sót rare features có signal mạnh nhưng ít xuất hiện

### Khoa học & Học thuyết

1. **Limited Theoretical Justification:** Bài báo không cung cấp analysis lý thuyết tại sao joint training tốt hơn ensemble. Giải thích dựa trên intuition (wide complement deep's weakness) nhưng chưa formal.

2. **Single Domain Evaluation:** Chỉ đánh giá trên Google Play (apps). Generalization đến recommendation tasks khác (movies, products) chưa rõ. Claim "should apply to generic recommender systems" chưa được validate thực nghiệm.

3. **Offline-Online Gap:** Offline AUC tăng nhỏ (0.002) nhưng online acquisition tăng 3.9%. Lý do chính xác chưa phân tích chi tiết—giả thuyết: online system explores new recommendations, learns from new user feedback. Cần ablation study để hiểu.

4. **Baseline Comparisons:** Chỉ so sánh với wide-only, deep-only, và ensemble (implicit). Không so sánh với factorization machines (FM) hoặc hybrid methods khác từ literature.

### Hạn chế Thực Tiễn

1. **Deployment Complexity:** Cần separate optimizers (FTRL for wide, AdaGrad for deep), vocabulary generator, warm-starting logic → increased engineering complexity.

2. **Real-time Learning:** Mô hình được retrain periodically (implicit)—không clear về frequency, impact của model staleness. Real-time online learning (streaming) không được xem xét.

3. **Feature Interaction Discovery:** Cross-product transformations phải được thiết kế. Bài báo không có systematic way để tìm ra transformations hiệu quả—dependency trên human expertise cao.

### Công trình tương lai

- Explore joint training cho andere architectures (RNNs, CNNs)
- Automatic feature interaction discovery thay vì manual engineering
- Theoretical analysis của joint training vs. ensemble
- Extended evaluation trên multiple domains (e-commerce, search ranking)
- Online learning mechanisms, model updating strategies

---

## Unresolved Questions

1. Làm sao để tự động discover effective cross-product transformations mà không cần manual feature engineering?
2. Warm-starting mechanism với embeddings từ previous model—có negative transfer risk không? Cần study impact kỹ.
3. Generalization tới domains khác ngoài Google Play (movies, e-commerce)—architecture có cần adjust không?
4. Offline AUC chỉ tăng 0.2% nhưng online acquisition +3.9%—root cause chính xác là gì? (exploration, online feedback learning, distribution shift?)
5. Feature vocabulary generation threshold—impact của việc loại bỏ rare features?
