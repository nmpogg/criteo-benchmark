# Review Paper: DQRM: Deep Quantized Recommendation Models

**ArXiv ID:** [2410.20046](https://arxiv.org/abs/2410.20046)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Large-scale DLRM models tiêu thụ memory khổng lồ (1TB+), gây thách thức cho cloud inference, edge deployment, và distributed training. Paper nghiên cứu **INT4 quantization toàn bộ DLRM** — giảm từ FP32 (32-bit) xuống INT4 (4-bit), đạt ~8× compression — và phát hiện rằng QAT không chỉ nén mà còn tạo **regularization effect** giúp tăng accuracy.

**Motivation:** INT4 quantization aggressive hơn INT8 nhưng nếu kết hợp đúng QAT technique, có thể vừa nén mạnh vừa cải thiện accuracy nhờ giảm overfitting.

## 2. Phương pháp sử dụng

**Quantization-Aware Training (QAT) cho INT4:**

1. **QAT Framework:** Train model biết về INT4 quantization từ đầu — model học cách compensate quantization error trong training
2. **2 Novel Techniques** cải thiện QAT cho embedding tables:
   - Tối ưu precision levels cho embedding tables
   - Tuning gradient behavior đặc biệt cho embeddings
3. **Distributed Training Optimization:**
   - INT8 gradient quantization cho embedding gradients
   - Gradient sparsification giảm communication overhead trong distributed training
4. **Regularization Effect:** QAT tạo implicit regularization, giảm overfitting — giải thích tại sao INT4 models có thể vượt FP32

## 3. Thành tựu đạt được

| Dataset | Accuracy | Model Size | Compression |
|---------|----------|------------|-------------|
| **Criteo Kaggle** | 79.07% | 0.27 GB (vs 2.16 GB FP32) | ~8× |
| **Criteo Terabyte** | 81.21% | 1.57 GB (vs 12.58 GB FP32) | ~8× |

- INT4 models **vượt trội FP32 baselines** về accuracy — nén mà còn tốt hơn
- Applicable cho 3 scenarios: cloud inference, edge devices, distributed training

## 4. Hạn chế

- **Training overhead:** QAT có chi phí tính toán cao hơn standard training — cần simulate quantization mỗi forward pass
- **Architecture-specific:** Chưa rõ tổng quát hóa cho architectures khác ngoài DLRM
- **Inference hardware:** Hiệu suất trên inference edge devices chưa được đánh giá chi tiết
- **Gradient sparsification risk:** Có thể mất thông tin quan trọng trong distributed training scenarios
- **Trade-off analysis:** Training time vs inference latency vs compression ratio chưa được fully explore
