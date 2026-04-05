# Review Paper: Product-based Neural Networks for User Response Prediction

**ArXiv ID:** [1611.00144](https://arxiv.org/abs/1611.00144)  
**Năm:** 2016  
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)  
**Tác giả:** Yanru Qu, Han Cai, Kan Ren, Weinan Zhang, Yong Yu (Shanghai Jiao Tong University), Ying Wen, Jun Wang (University College London)  
**Hội nghị:** ICDM 2016

---

## 1. Paper này đang nghiên cứu gì?

Bài báo tập trung vào **dự đoán user response** (clicks, conversions) trên dữ liệu **multi-field categorical** trong quảng cáo online, hệ thống gợi ý, và tìm kiếm web. Vấn đề cốt lõi:

**Thách thức dữ liệu:**
- Dữ liệu thực tế là multi-field categorical (ví dụ: [Weekday=Tuesday, Gender=Male, City=London])
- One-hot encoding tạo ra vector **cực kỳ thưa, siêu chiều cao** (sparse high-dimensional)
- Ví dụ: 3 fields → concatenate [0,1,0,0,0,0,0] | [0,1] | [0,0,1,0,...,0,0] → hàng trăm ngàn chiều

**Giới hạn của các mô hình hiện tại:**
- **Linear logistic regression:** Chỉ học low-order feature combinations, không capture high-order latent patterns → low accuracy
- **Gradient boosting (GBDT):** Cần feature engineering thủ công để capture high-order patterns; không tự động học
- **Factorization machines (FM):** Tốn feature engineering, chỉ model pairwise interactions
- **Deep neural networks (DNNs):** Không áp dụng trực tiếp được vì input cực thưa; MLPs với embedding + concatenation không hiệu quả explore feature interactions

**Hiện tượng cụ thể:** Standard MLPs sử dụng phép cộng ("add") để kết hợp signals → mất thông tin về **local dependencies** giữa fields; các tác giả khác (FM, prior work) chứng minh vector "product" operations hiệu quả hơn.

**Giải pháp:** Bài báo đề xuất **Product-based Neural Networks (PNN)** — kết hợp embedding layer (convert sparse → dense), product layer (capture inter-field feature interactions via products), và fully-connected layers (explore high-order patterns) để tự động học complex feature representations.

---

## 2. Phương pháp sử dụng

### Kiến trúc PNN

**Tổng quan (từ dưới lên):**

```
Input: [Field 1, Field 2, ..., Field N] (one-hot encoded, sparse)
    ↓
Embedding Layer (Field-wise Fully Connected)
    ↓ Output: [f_1, f_2, ..., f_N] (N × M embedding vectors, M=embedding dim)
    ↓
Product Layer (Pair-wise Connected, generates z and p)
    ↓
Hidden Layer 1 (Fully Connected, ReLU)
    ↓
Hidden Layer 2 (Fully Connected, ReLU)
    ↓
Output Unit (Sigmoid) → ŷ ∈ (0,1) (predicted CTR)
```

**Chi tiết từng thành phần:**

**1. Embedding Layer:**
- Input: one-hot feature vector x, x[start_i : end_i] cho field i
- Fully connected với field i: f_i = W'_i × x[start_i : end_i], f_i ∈ ℝ^M
- Output: N embedding vectors, mỗi 10-50 chiều (paper dùng M=10 order embedding)
- Benefit: Convert sparse → dense, learn distributed representations tự động

**2. Product Layer (Tâm yếu):**
Với constant signal "1" để preserve linear signals:

- **Linear signals z:** z = [f_1, f_2, ..., f_N] (N embedding vectors)
- **Quadratic signals p:** p = {p_{i,j}}, i,j = 1...N, với p_{i,j} = g(f_i, f_j) (pairwise feature interaction)

Hai biến thể:

**A. Inner Product-based Neural Network (IPNN):**
- g(f_i, f_j) = ⟨f_i, f_j⟩ (vector inner product → scalar)
- p ∈ ℝ^{N×N} (symmetric matrix)
- l_n^p = Σ_i Σ_j (W^p_n)_{i,j} p_{i,j}
- **Complexity Problem:** O(N²(D_1 + M)) time, O(D_1 N(M+N)) space (quadratic in N)
- **Solution - Matrix Factorization:** Assume W^p_n = θ^n (θ^n)^T (rank-1 decomposition)
  - Simplify: W^p_n ⊙ p = ⟨Σ_i δ^n_i, Σ_i δ^n_i⟩, với δ^n_i = θ^n_i f_i
  - Reduce complexity: O(D_1 M N) time, O(D_1 M N) space (linear in N)
- **General K-order decomposition:** θ^i_n ∈ ℝ^K, W^p_n ⊙ p = Σ_i Σ_j ⟨θ^i_n, θ^j_n⟩ ⟨f_i, f_j⟩ (K times complexity)

**B. Outer Product-based Neural Network (OPNN):**
- g(f_i, f_j) = f_i f_j^T (vector outer product → matrix, M×M)
- p ∈ ℝ^{N×N}, mỗi p_{i,j} ∈ ℝ^{M×M}
- **Naive complexity:** O(D_1 M² N²) (quá cao)
- **Optimization - Superposition:** p = Σ_i Σ_j f_i f_j^T = f_Σ (f_Σ)^T, với f_Σ = Σ_i f_i
  - p ∈ ℝ^{M×M} (symmetric)
  - Reduce: O(D_1 M(M+N)) time, O(D_1 M(M+N)) space (manageable)

**3. First Hidden Layer:**
- l^1 = relu(l_z + l_p + b_1), l^1 ∈ ℝ^{D_1}
- l_z: linearly weighted z (preserve linear signals)
- l_p: quadratic signals từ product layer
- Combine: add linear + quadratic signals → ReLU activation

**4. Second Hidden Layer & Output:**
- l^2 = relu(W^2 l^1 + b^2), l^2 ∈ ℝ^{D_2}
- ŷ = σ(W^3 l^2 + b^3) ∈ (0,1)
- Sigmoid cho binary classification

**Training:**
- Loss: L(y, ŷ) = -y log ŷ - (1-y) log(1-ŷ) (cross-entropy, log loss)
- Optimizer: SGD
- Regularization: L2 regularization cho LR/FM, dropout (rate 0.5) cho neural networks
- Activation: ReLU (sparse activation, efficient gradient, no vanishing/exploding gradient)

### Variants & Comparisons

**PNN* (Concatenation Variant):**
- Product layer concatenates inner product + outer product outputs
- Flexible nhưng complexity cao hơn

**Comparison with FM & FNN:**
- **FM:** PNN ⊃ FM nếu remove l_p (no hidden layers, uniform weights) → degenerate case
- **FNN:** PNN ⊃ FNN (w/o product layer) + product layer → FNN là special case

---

## 3. Thành tựu đạt được

### Dữ liệu Thực Nghiệm

**Dataset 1: Criteo (1TB Click Log)**
- 7 consecutive days training, 1 day test
- Negative down-sampling (w=1000): 79.38M instances, 1.64M feature dimensions

**Dataset 2: iPinYou**
- 10 days ad click logs
- 3 last days test, rest training (per advertiser)
- 19.50M instances, 937.67K feature dimensions

### Kết quả Chi Tiết

**Table I - Criteo Dataset:**

| Model | AUC | Log Loss | RMSE | RIG |
|-------|-----|----------|------|-----|
| LR | 71.48% | 0.1334 | 9.362e-4 | 6.680e-2 |
| FM | 72.20% | 0.1324 | 9.284e-4 | 7.436e-2 |
| FNN | 75.66% | 0.1283 | 9.030e-4 | 1.024e-1 |
| CCPM | 76.71% | 0.1269 | 8.938e-4 | 1.124e-1 |
| **IPNN** | **77.79%** | **0.1252** | **8.803e-4** | **1.243e-1** |
| OPNN | 77.54% | 0.1257 | 8.846e-4 | 1.211e-1 |
| PNN* | 77.00% | 0.1270 | 8.988e-4 | 1.118e-1 |

**Table II - iPinYou Dataset:**

| Model | AUC | Log Loss | RMSE | RIG |
|-------|-----|----------|------|-----|
| LR | 73.43% | 5.581e-3 | 5.350e-07 | 7.353e-2 |
| FM | 75.52% | 5.504e-3 | 5.343e-07 | 8.635e-2 |
| FNN | 76.19% | 5.443e-3 | 5.285e-07 | 9.635e-2 |
| CCPM | 76.38% | 5.522e-3 | 5.343e-07 | 8.335e-2 |
| IPNN | 79.14% | 5.195e-3 | 4.851e-07 | 1.376e-1 |
| **OPNN** | **81.74%** | **5.211e-3** | **5.293e-07** | **1.349e-1** |
| PNN* | 76.61% | 4.975e-3 | 4.819e-07 | 1.740e-1 |

**Improvements Chính:**

- **IPNN trên Criteo:** AUC +6.31 điểm so với FNN, +5.59 so với CCPM (baseline gần nhất)
- **OPNN trên iPinYou:** AUC +5.55 so với FNN, +5.36 so với CCPM (huge improvement)
- **Across metrics:** Log Loss, RMSE, RIG consistency high improvements
- **Statistical significance:** t-test p-values < 10^{-6} vs. LR/FM, < 10^{-5} vs. CCPM (highly significant)

**Learning Curves (iPinYou):**
- PNN models converge faster than LR/FM
- IPNN/OPNN better convergence than FNN/CCPM across iterations
- Stable learning, no oscillation

### Ablation Study Insights

**1. Embedding Dimension:**
- Tested orders 2, 10, 50, 100
- Paper uses 10-order embedding (balance between expressiveness & memory)
- Higher orders → overfitting risk

**2. Network Depth:**
- Tested hidden layers: 1, 3, 5, 7
- **Optimal: 3 hidden layers** (best generalization)
- Deeper networks (5, 7) → overfitting
- Product/convolution layers as "representation layers" → capture complex patterns efficiently

**3. Activation Functions:**
- Sigmoid, tanh, ReLU comparison
- **ReLU performs best** (sparse activation, efficient gradient, no vanishing/exploding gradient)
- tanh > sigmoid on both datasets

**4. Dropout Rate:**
- Tested 0.1 to 0.9 on OPNN (Criteo)
- **Optimal: 0.5** (proven effective for regularization)

**Dataset-specific Patterns:**
- **IPNN better on Criteo:** Inner product captures fine-grained interactions
- **OPNN dominant on iPinYou:** Outer product's expressiveness shine on sparser dataset
- **PNN* underperforms:** Concatenation doesn't add enough benefit vs. complexity tradeoff

---

## 4. Hạn chế

### Kỹ thuật

1. **PNN* Underwhelming Results:** Concatenating inner + outer products không cho lợi ích rõ rệt. Paper suggests IPNN + OPNN đủ để capture feature interactions → contradiction, cần clear guidelines khi chọn IPNN vs OPNN.

2. **Embedding Initialization:** Không pre-training (khác FNN dùng pre-trained FM). Impact của random initialization vs. FM pre-training không compare. Có thể miss signal từ factorization.

3. **Feature Engineering Still Required:** Mặc dù automatic interaction learning, still need:
   - Field definition (which categorical features group lại?)
   - Vocabulary generation (minimum frequency threshold để include feature)
   - One-hot encoding scheme
   → Not fully end-to-end

4. **Complexity Analysis Not Complete:**
   - IPNN: Matrix factorization giảm O(N²) → O(N), nhưng K-order decomposition hầu chưa explored
   - OPNN: Superposition trik reduce O(N² M²) → O(NM(M+N)), nhưng still expensive khi M, N large
   - Scalability giới hạn cho very high-dimensional inputs

5. **Limited Hyperparameter Exploration:**
   - Fixed 3 hidden layers, 10-order embedding được declare "best" nhưng chưa systematic grid search
   - Dropout rate optimal 0.5 chỉ found empirically
   - Learning rate, batch size, regularization strength không reported

### Khoa học & Học thuyết

1. **Unclear Feature Interaction Mechanism:** 
   - Tại sao vector products (⟨f_i, f_j⟩ vs. f_i f_j^T) hiệu quả capture multi-field categorical interactions?
   - Analogy "AND"/"OR" gates (multiplication = "AND", addition = "OR") intuitive nhưng formal analysis lacking
   - No theoretical justification why products > MLPs with add operations

2. **Comparison Gaps:**
   - No comparison with factorization-based deep models (FM-based DNNs)
   - No comparison with other deep architectures (RNNs, attention mechanisms)
   - CCPM (convolutional model) underperforms, nhưng convolution tuy chỉ local features—fair comparison?

3. **Dataset Specificity:**
   - Chỉ evaluated trên ad click prediction (CTR)
   - Generalization to other user response tasks (conversions, dwell time) unclear
   - Only 2 datasets (both ad-related) → limited scope

4. **Statistical Testing:** 
   - t-test report p-values nhưng no confidence intervals
   - No cross-validation scheme explicitly described (implicit train/test split)
   - Single run results or averaged over multiple seeds? (not mentioned)

5. **Offline Evaluation Only:**
   - No online A/B testing (unlike Wide & Deep paper)
   - Offline metrics may not reflect online user satisfaction
   - Real-world performance impact unknown

### Hạn chế Thực Tiễn

1. **Serving Complexity:** Paper không discuss model serving, latency, throughput requirements. How does PNN scale to billions of predictions/day?

2. **Feature Representation Gap:**
   - Assume fields are independent (field-wise embedding connection) → may miss cross-field early interactions
   - "Local dependencies" preserve via product layer nhưng mechanism not fully clear

3. **Negative Down-sampling (Criteo):**
   - Applied down-sampling ratio w=1000 → biased training distribution
   - Recalibration formula q = p/(p + (1-p)/w) used at test time
   - Impact của biased training on model robustness not analyzed

4. **Product Layer Design Arbitrariness:**
   - Why inner product vs. outer product? (paper only empirical comparison)
   - Could other product types (element-wise, Hadamard) work better?
   - No principled way to choose

5. **Embedding Dimension Scaling:**
   - Paper fixes embedding order = 10 for "consistency with FM"
   - But deep learning embeddings ≠ FM latent factors; may need different dimensionality

### Công trình tương lai

- Explore PNN với more general/complex product layers
- Explain & visualize learned embedding vectors
- Apply node representations to other tasks
- Online evaluation & A/B testing
- Theoretical analysis of product operations for categorical data
- Integration with other techniques (attention, graph neural networks)
- End-to-end learning without manual field engineering

---

## Unresolved Questions

1. **IPNN vs. OPNN Selection:** Các dataset nào nên dùng IPNN vs. OPNN? Có heuristic hay principled way không?

2. **Embedding Pre-training:** Có nên pre-train embeddings từ FM trước như FNN? Impact tới convergence speed, final accuracy?

3. **Feature Interaction Types:** Product operations (inner/outer) assumption tối ưu cho categorical multi-field data? Có interaction types khác thích hợp hơn?

4. **Scalability at Production:** Khi N (fields) hoặc M (embedding dim) rất lớn, complexity O(D_1 M(M+N)) hay O(D_1 MN) có thực tế không?

5. **Generalization Beyond CTR:** PNN có effective cho user response tasks khác (conversion, engagement)? Architecture cần modify?

6. **K-order Decomposition:** K-order matrix factorization (eq. 13) được mention nhưng không experiment. Trade-off between expressiveness & complexity?

7. **Statistical Significance - Practical Impact:** p-values < 10^{-6} statistically significant, nhưng AUC improvement 2-5 điểm → equivalent to bao nhiêu % revenue/user satisfaction gain?

8. **Offline-Online Gap:** Similar to Wide & Deep—offline metrics tốt nhưng online performance? (paper chưa test)
