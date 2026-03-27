# Review Paper: DimGrow: Memory-Efficient Field-level Embedding Dimension Search

**ArXiv ID:** [2505.12683](https://arxiv.org/abs/2505.12683)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết vấn đề tối ưu hóa embedding dimensions across feature fields trong recommendation systems. Vấn đề cốt lõi là các fields khác nhau yêu cầu số lượng dimensions khác nhau - một số features cần representations phức tạp (64+ dimensions), trong khi những fields đơn giản chỉ cần 1-2 dimensions. Tuy nhiên, phương pháp traditional dùng fixed dimensions cho tất cả fields dẫn đến lãng phí bộ nhớ không cần thiết.

Neural Architecture Search (NAS) approaches như SuperNets có thể enumerate tất cả dimension combinations, nhưng chúng tính toán không khả thi - yêu cầu memory exponential theo số lượng fields. Ví dụ, với 39 fields Criteo dataset, số combinations đạt 10^30+. Hiện tại không có phương pháp efficient nào có thể explore embedding dimension space mà không gây ra memory explosion.

Paper này nhằm develop progressive expansion strategy loại bỏ dependency vào SuperNets, cho phép efficient exploration của dimension search space với training memory reduction của 19-23% so với baselines.

## 2. Phương pháp sử dụng

DimGrow propose progressive dimension expansion strategy thay vì exhaustive enumeration. Approach này bắt đầu với minimal one-dimensional embeddings per feature field, sau đó gradually expand dimensions dựa trên learned importance scores.

**Cơ chế chính - Shuffle Gate:** DimGrow extend Shuffle Gate (originally cho feature selection) lên dimension-level evaluation. Mỗi embedding dimension có learnable gate parameter đo lường importance bằng cách assess impact của shuffling dimension đó cross batch samples. Gate value gần 1 indicates significant impact (high importance), near 0 suggests minimal importance (low importance).

Gating function combine original và shuffled embedding values:
- Original dimension weighted by gate parameter: g_{i,k}
- Shuffled dimension weighted by (1 - g_{i,k})
- L1 regularization encourage polarization towards 0 or 1

Natural polarization property critical - gates converge tới extreme values thay vì intermediate ranges, enabling clear importance discrimination mà không cần extensive hyperparameter tuning.

**Progressive Expansion Algorithm:**
1. **Initialization:** Mỗi feature field bắt đầu với single embedding dimension
2. **Expansion condition:** Khi ALL currently-used dimensions exceed upper threshold (T_up = 0.6), thêm new dimension tới field's embedding table
3. **Reduction condition:** Nếu dimension's importance dưới lower threshold (T_down = 0.01), dimension được prune
4. **Regularization:** Dimension-wise decaying L1 penalty `|g_{i,k}|/(k+1)` facilitate growth của higher-order dimensions bằng applying weaker regularization pressure

**Dynamic Architecture:** Maintain dynamic embedding tables expand/contract during training, với adaptation layer cung cấp fixed-dimension input tới backbone model despite varying embedding dimensions. Concatenated embeddings varying widths pass qua adaptive weight matrices transform variable-width inputs thành consistent backbone input dimensions.

## 3. Thành tựu đạt được

Experimental validation trên ba recommendation datasets: Aliccp, Avazu, Criteo (23-39 feature fields):

**Hiệu suất dự đoán:**
- DimGrow đạt competitive hoặc superior AUC across compression ratios (10%, 20%, 50% of baseline parameters)
- Outperforms SSEDS và DimReg consistently, particularly tại high compression ratios
- Exceeds AutoDim và OptEmbed-D performance enable higher compression ratios

**Hiệu quả bộ nhớ:**
- GPU memory reduction: 19-23% trên datasets với large embedding tables
- Trên Criteo-32: maintain constant memory (18.8GB) while SuperNet-based methods scale tới 33.6GB
- Computational overhead modest; sometimes faster than baseline training trên large embedding scenarios

**Comparative analysis:** DimGrow eliminate need cho memory-intensive SuperNets during dimension search phase, making practical để optimize embedding architectures trên production-scale datasets. Progressive strategy efficiently explore search space while maintaining substantially lower memory overhead.

## 4. Hạn chế

Phương pháp phụ thuộc vào chọn thresholds (T_up = 0.6, T_down = 0.01) - sensitivity analysis tới hyperparameters không chi tiết. Shuffle Gate approach có thể không work tốt cho datasets với features có high statistical dependence - shuffling một dimension có thể not capture true importance nếu features highly correlated.

Framework assumes fixed backbone models - adaptation strategy của fixed-width input layer có thể not efficient nếu embedding dimensions vary dramatically. Decaying L1 regularization schedule cố định có thể not optimal cho tất cả datasets. Paper không discuss dynamic thresholds adjustment dựa trên training progress.

Online learning scenarios hoặc stream learning với dynamic feature space không explored. Integration với modern embedding compression techniques (quantization, factorization) cần investigation. Future work should explore meta-learning approaches để learn importance scoring functions generalize across datasets, và incorporate theoretical analysis về convergence properties.
