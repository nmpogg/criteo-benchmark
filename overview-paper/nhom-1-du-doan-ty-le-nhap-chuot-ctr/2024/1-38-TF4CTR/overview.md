# Review Paper: TF4CTR: Twin Focus Framework for CTR Prediction via Adaptive Sample Differentiation

**ArXiv ID:** [2405.03167](https://arxiv.org/abs/2405.03167)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Xử lý vấn đề mô hình coi đều tất cả samples:
- Thiên về easy samples
- Differentiated encoders nhận tín hiệu supervision giống nhau

## 2. Phương pháp sử dụng

- Sample Selection Embedding Module (SSEM): phân biệt samples ở bottom layer
- Twin Focus (TF) Loss: supervision signals khác nhau cho simple & complex encoders
- Dynamic Fusion Module (DFM): kết hợp dynamic feature interaction

## 3. Thành tựu đạt được

- Hiệu suất cải thiện trên 5 real-world datasets
- Model-agnostic, nâng cao các baselines khác nhau
- Chấp nhận TCSS

## 4. Hạn chế

- Không thảo luận computational overhead
- Hiệu suất cải thiện khiêm tốn trên một số datasets
- Phức tạp điều chỉnh hyperparameters
