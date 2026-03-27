# Review Paper: Hierarchical LoRA MoE for Efficient CTR Model Scaling

**ArXiv ID:** [2510.10432](https://arxiv.org/abs/2510.10432)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Paper này giải quyết một trade-off cơ bản trong CTR model scaling: làm thế nào để tăng model expressiveness mà không phải tăng computational cost một cách tuyến tính.

Có hai cách truyền thống để scale CTR models:
- **Vertical scaling**: Stack thêm layers để tăng depth. Điều này cải tiến expressiveness nhưng tăng computational cost đáng kể.
- **Horizontal scaling via Mixture of Experts (MoE)**: Activate chỉ một subset của experts cho mỗi input, giúp efficient scaling. Tuy nhiên, traditional MoE routing thường bottleneck tại output computation của layer trước.

Vấn đề đặt ra: làm thế nào để combine lợi ích của cả vertical scaling (expressiveness tốt) và horizontal scaling (efficiency cao) trong một framework thống nhất? Đây là câu hỏi quan trọng vì trong production systems, compute budget là resource quý giá.

## 2. Phương pháp sử dụng

Tác giả giới thiệu **HiLoMoE (Hierarchical LoRA MoE)**, kết hợp hai kỹ thuật cốt lõi:

**Lightweight rank-1 experts for parameter-efficient horizontal scaling**: Thay vì sử dụng full dense experts (tốn tài nguyên), HiLoMoE sử dụng rank-1 LoRA (Low-Rank Adaptation) experts. Mỗi expert chỉ cần lưu trữ two rank-1 matrices (tương tự LoRA trong LLM fine-tuning), giảm số parameters cần học drastically.

**Hierarchical routing with prior layer scores**: Thay vì routing based on output của current layer (traditional approach), HiLoMoE routes based on scores từ prior layer. Điều này cho phép:
- Parallel execution across multiple MoE layers (vì routing decisions được made sớm hơn)
- Combinatorially diverse expert compositions - khác nhau từ layer sang layer, cho phép learn richer interactions

**Three-stage training framework**: Paper propose một principled training strategy với 3 stages để ensure stable optimization:
1. Pre-training experts
2. Router training
3. Joint fine-tuning

Kỹ thuật này đảm bảo expert diversity và stable convergence, tránh tình trạng một vài experts được over-utilized.

## 3. Thành tựu đạt được

HiLoMoE đạt được cải tiến both về accuracy lẫn efficiency trên multiple datasets:

**AUC improvement: +0.20%** - Trên non-MoE baseline, HiLoMoE đạt 0.20% AUC improvement. Đây là consistent gain so với baseline, chứng minh rằng hierarchical routing + rank-1 experts thực sự có lợi.

**FLOPs reduction: 18.5%** - Floating-point operations giảm 18.5%, cho thấy model hiệu quả hơn về computational cost. Đây là significant vì 18.5% FLOPs reduction trực tiếp dịch sang faster inference và lower serving cost.

**Evaluation scope: Four public datasets** - Paper evaluate trên 4 public CTR datasets (tuy không nêu tên cụ thể trong abstract), cho thấy findings có generalization.

**Balanced improvements**: HiLoMoE đạt cả AUC improvement và FLOPs reduction đồng thời, là rare case trong ML nơi thường phải trade-off giữa accuracy và efficiency.

## 4. Hạn chế

Mặc dù HiLoMoE có những kết quả tốt, nhưng vẫn có những hạn chế cần xem xét:

**Về training complexity**: Paper nêu "three-stage training framework" nhưng không rõ ràng discuss về implementation complexity. Ba-stage training có thể khó tune hyperparameters và replicate, so với simple end-to-end training.

**Về rank-1 limitation**: Sử dụng rank-1 LoRA experts là parameter-efficient, nhưng có thể limitation về expressive power. Rank-1 matrices có thể không đủ capture complex interactions trong một số cases. Cần test empirical performance trên very high-dimensional CTR data.

**Về routing overhead**: Hierarchical routing dựa trên "prior layer scores" - paper không discuss về computational overhead của routing mechanism itself. Mặc dù nói là "parallel execution", nhưng routing computation vẫn phải happen, có thể become bottleneck nếu không implement efficiently.

**Về baseline comparison**: Paper compare với "non-MoE baseline" nhưng không specify baseline architecture rõ ràng. Cần so sánh với other scaling approaches (deeper networks, wider networks, other MoE variants) để có full picture của effectiveness.

**Về online evaluation**: Không mention online/production results. 0.20% AUC improvement là modest, cần verify nếu translates thành meaningful CTR/revenue gains trong production.
