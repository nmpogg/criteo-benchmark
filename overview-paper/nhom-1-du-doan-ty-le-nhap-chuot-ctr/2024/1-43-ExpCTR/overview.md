# Review Paper: ExpCTR: Explainable CTR Prediction via LLM Reasoning

**ArXiv ID:** [2412.02588](https://arxiv.org/abs/2412.02588)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết thiếu tính minh bạch trong quyết định hệ thống gợi ý:
- Phương pháp post-hoc phải xây dựng dữ liệu đặc biệt, gây lo ngại độ tin cậy

## 2. Phương pháp sử dụng

- Tích hợp LLM trực tiếp vào quá trình dự đoán CTR (không post-hoc)
- LC alignment: giải thích phản ánh ý định người dùng
- IC alignment: nhất quán với mô hình CTR truyền thống
- LoRA + quy trình 3 giai đoạn lặp lại

## 3. Thành tựu đạt được

- Cải thiện độ chính xác dự đoán & khả năng giải thích trên 3 dataset
- Loại bỏ nhu cầu dataset giải thích mở rộng

## 4. Hạn chế

- Không nêu rõ hạn chế trong abstract
- Latency & complexity của LLM reasoning ảnh hưởng CTR prediction
