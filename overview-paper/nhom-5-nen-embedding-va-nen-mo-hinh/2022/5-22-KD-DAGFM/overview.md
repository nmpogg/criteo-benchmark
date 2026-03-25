# Review Paper: KD-DAGFM: Directed Acyclic Graph Factorization Machines for CTR via Knowledge Distillation

**ArXiv ID:** [2211.11159](https://arxiv.org/abs/2211.11159)
**Năm:** 2022
**Tác giả:** Tencent (WeChat team)
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Các mô hình CTR prediction phức tạp (teacher models) cho accuracy cao nhưng **computationally expensive** (cao FLOPs), không phù hợp cho real-time inference trong production. Feature interactions bậc cao phức tạp nhưng cần được mô hình hóa efficiently.

**Motivation:** Compress complex interaction models thành **lightweight student models** bằng knowledge distillation, đạt cả efficiency và accuracy cho web-scale systems (WeChat, Criteo-scale với billions of features).

## 2. Phương pháp sử dụng

**DAGFM + Knowledge Distillation framework:**

1. **DAGFM (Directed Acyclic Graph FM):**
   - Biểu diễn feature interactions dưới dạng DAG — mỗi node = feature, edges = interactions
   - **Dynamic Programming algorithm** để tính feature interactions approximately lossless
   - Proof: Có thể capture arbitrary explicit feature interactions từ teacher networks

2. **Knowledge Distillation:**
   - **Teacher:** Complex model (DeepFM, xDeepFM, etc.) học full feature interactions
   - **Student:** Lightweight DAGFM model — nhẹ hơn nhiều lần
   - Transfer knowledge từ teacher → student qua distillation loss

3. **KD-DAGFM+ (enhanced variant):**
   - Capture cả **explicit interactions** (learnable feature crosses) lẫn **implicit interactions** (từ complex teacher embeddings)
   - Generalized để hoạt động với bất kỳ teacher model nào

## 3. Thành tựu đạt được

| Metric | Kết quả |
|--------|---------|
| **FLOPs** | Chỉ <21.5% FLOPs so với SOTA (5× reduction) |
| **Accuracy** | Gần như không mất mát, competitive với teacher |
| **Datasets** | 4 real-world datasets (Criteo + WeChat billions features) |
| **Theory** | DP proof cho approximately lossless learning |
| **Code** | Công khai mã nguồn |

Vượt trội hơn baselines (DeepFM, xDeepFM, etc.) trên cả offline và online experiments.

## 4. Hạn chế

- **Phụ thuộc teacher:** Hiệu suất student bị giới hạn bởi chất lượng teacher model — teacher kém → student kém
- **Tuning phức tạp:** Cần tuning để cân bằng explicit + implicit interactions trong KD-DAGFM+, distillation temperature, loss weights
- **DAG structure:** Xác định optimal DAG structure vẫn là challenge, chưa có automated DAG search
- **Limited interaction types:** DAG approach có thể không capture tất cả complex high-order interactions
- **Distillation cost:** Chi phí training teacher + distillation chưa được phân tích chi tiết
