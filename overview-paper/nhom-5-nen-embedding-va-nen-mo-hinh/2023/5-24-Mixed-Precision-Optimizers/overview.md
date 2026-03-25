# Review Paper: Memory Efficient Mixed-Precision Optimizers

**ArXiv ID:** [2309.12381](https://arxiv.org/abs/2309.12381)
**Năm:** 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Training neural networks với single-precision (fp32) tiêu tốn bộ nhớ lớn vì optimizers (Adam, SGD) phải lưu bản sao fp32 của parameters. Giảm precision xuống fp16 gây divergence. Các phương pháp mixed-precision hiện tại vẫn phải giữ full-precision copy, lãng phí bộ nhớ. Bài báo đề xuất kỹ thuật loại bỏ hoàn toàn bản sao fp32, giảm memory footprint mà vẫn duy trì accuracy thông qua "extra-bit precision" và fused backward pass.

## 2. Phương pháp sử dụng

Hai kỹ thuật chính được đề xuất:

1. **Loại bỏ bản sao single-precision**: Chỉ duy trì parameters ở half-precision (fp16), không cần giữ fp32 copy. Thêm "extra-bit precision" (8-16 bits) để ngăn divergence — ít hơn nhiều so với full fp32 copy nhưng đủ để duy trì numerical stability.

2. **Fused backward pass**: Tích hợp optimizer steps trực tiếp vào quá trình backpropagation thay vì lưu gradient values riêng biệt rồi mới update — giảm thêm memory footprint vì không cần buffer cho gradients.

Triển khai qua custom CUDA kernels cho SGD momentum, Adam, và AdamW.

## 3. Thành tựu đạt được

| Model | Dataset | Kết quả |
|-------|---------|---------|
| ResNet-18 | CIFAR-10 | 94.06% accuracy; 20min training (vs 42min fp32) |
| BERT-base | GLUE | 11% memory savings trên MNLI, QNLI, MRPC |
| DLRM | Kaggle-Criteo | Matched fp32 accuracy với 8 extra-bits |
| DCGAN | LSUN-bedroom | Tốt hơn standard bf16 training |
| T5 (large) | GLUE | 11% memory reduction; <3% time increase |

- Peak memory reduction: lên tới 54% (synthetic), **20-25%** thực tế
- Training speedup: lên tới **16%** (ResNet-18), 2-10% với fused optimizers
- Duy trì accuracy comparable với fp32 training, ngăn divergence so với fp16-only

## 4. Hạn chế

- Phụ thuộc custom CUDA kernels → chỉ hoạt động tốt trên GPU NVIDIA, giảm portability
- Hiệu suất phụ thuộc hardware: tốt trên A100, kém hơn trên V100
- Không có phân tích tradeoff giữa số extra-bits vs accuracy cho các model khác nhau
- Overhead của extra-bit precision management không được định lượng rõ
- Scalability tới extremely large models (>10B parameters) chưa kiểm chứng
