# Review Paper: FLIP: Fine-grained Alignment between ID-based Models and Pretrained Language Models for CTR Prediction

**ArXiv ID:** [2310.19453](https://arxiv.org/abs/2310.19453)
**Năm:** 2024 | **Venue:** RecSys 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết khoảng cách giữa hai paradigm bổ sung nhau. **ID-based models** capture collaborative signals từ tabular features xuất sắc nhưng mất thông tin ngữ nghĩa do one-hot encoding. **Pretrained Language Models (PLMs)** giữ semantic knowledge từ text nhưng khó capture field-wise collaborative signals. Các phương pháp hiện tại dùng instance-level contrastive learning (global views) nhưng thiếu **fine-grained feature-level alignment** giữa hai paradigm.

## 2. Phương pháp sử dụng

**FLIP Framework:**

- **Jointly masked tabular/language modeling**: Mask data ở một modality (IDs hoặc tokens) → khôi phục bằng thông tin từ modality kia. Thiết lập **feature-level interaction qua mutual information extraction**
- Vượt qua hạn chế contrastive learning mức instance — học alignment ở mức feature chi tiết hơn
- **Adaptive output combination**: Jointly finetune ID-based model và PLM, kết hợp outputs optimal
- **Model-agnostic**: Tương thích với các ID-based models (DCN, DeepFM) và PLMs (BERT, RoBERTa) khác nhau

## 3. Thành tựu đạt được

- Vượt trội **SOTA baselines trên 3 real-world datasets**
- Chấp nhận tại **RecSys 2024** — venue hàng đầu recommendation systems
- Tương thích cao với nhiều architectures khác nhau — flexibility cho production
- Feature-level alignment hiệu quả hơn instance-level contrastive approaches

## 4. Hạn chế

- Cụ thể % AUC gain, LogLoss reduction không công bố trong abstract
- Chi phí jointly masked modeling (masking, recovery, alignment) cao hơn contrastive đơn giản
- Yêu cầu cả ID model + PLM → **tăng deployment complexity đáng kể**
- Hiệu quả trên domains không có rich textual features chưa rõ
