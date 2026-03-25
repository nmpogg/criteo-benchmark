# Review Paper: FIITED: Feature Importance Informed Tensor Embedding Dimension Optimization During Training

**ArXiv ID:** [2401.04408](https://arxiv.org/abs/2401.04408)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding vectors trong recommendation models không đều quan trọng — một số dimensions có impact lớn đến prediction, số khác ít quan trọng và lãng phí memory. Paper nghiên cứu cách **pruning dimensions ngay trong quá trình training** dựa trên feature importance, thay vì post-training compression.

**Motivation:** In-training pruning cho phép model **adapt** trong khi học, tốt hơn post-hoc pruning. Thách thức là detect feature importance chính xác và dynamic dimension pruning không ảnh hưởng model quality.

## 2. Phương pháp sử dụng

**FIITED — Fine-grained In-Training Embedding Dimension optimization:**

1. **Feature Importance Identification:**
   - **Frequency-based:** Tần suất feature xuất hiện trong data
   - **Gradient-based:** Độ lớn gradient cho biết ảnh hưởng đến loss function
   - Combined signals để prioritize critical embeddings

2. **In-Training Dimension Pruning:**
   - Dynamically giảm embedding dimensions cho features ít quan trọng khi training
   - Fine-grained: pruning ở level từng dimension (không phải feature level)
   - Gradual pruning — không cắt đột ngột

3. **Novel Embedding Storage:**
   - **Virtually-hashed physically-indexed hash tables** cho phép variable embedding dimensions
   - Enable efficient dimension pruning trong training phase
   - Support mixed-dimension embeddings trong cùng một table

## 3. Thành tựu đạt được

| Metric | Kết quả |
|--------|---------|
| **Industry models** | Giảm 65%+ embedding table size |
| **Public datasets** | 2.1× đến 800× size reduction |
| **Accuracy** | Negligible accuracy loss, thậm chí cải thiện |
| **Throughput** | Cải thiện nhờ giảm memory footprint |

Outperforms existing in-training embedding pruning approaches.

## 4. Hạn chế

- **Irregular memory access:** Dynamic dimension pruning tạo irregular access patterns — khó optimize trên GPUs hiện tại
- **Importance scoring accuracy:** Có thể prune wrong dimensions nếu importance scoring không chính xác
- **Computational overhead:** Gradient computation cho variable-dimension embeddings chưa fully quantified
- **Virtual hashing overhead:** Memory indirection từ hashing mechanism có thể tạo latency
- **Hardware compatibility:** Hard to implement efficiently trên current GPU architectures do irregular access patterns
