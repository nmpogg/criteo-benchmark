# Review Paper: FLIP: Fine-grained Alignment between ID-based Models and Pretrained Language Models for CTR Prediction

**ArXiv ID:** [2310.19453](https://arxiv.org/abs/2310.19453)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Kết nối hai paradigm: ID-based models và pretrained language models:
- ID-based: collaborative signals từ tabular features
- PLMs: semantic knowledge từ text

## 2. Phương pháp sử dụng

- Jointly masked tabular/language modeling task
- Masked data từ một modality được khôi phục bằng modality khác
- Adaptive combination outputs từ ID-based models & PLMs
- Chấp nhận RecSys 2024

## 3. Thành tựu đạt được

- Vượt trội baselines trên 3 real-world datasets
- Tương thích với các ID-based models & PLM architectures khác nhau

## 4. Hạn chế

- Phức tạp implementation (dual-modality training + adaptive fusion)
- Scalability không rõ ràng
- Yêu cầu tài nguyên tính toán lớn hơn mô hình đơn
