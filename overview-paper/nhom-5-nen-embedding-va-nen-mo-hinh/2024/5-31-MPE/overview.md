# Review Paper: MPE: Mixed-Precision Embeddings for Large-Scale Recommendation Models

**ArXiv ID:** [2409.20305](https://arxiv.org/abs/2409.20305)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết vấn đề bộ nhớ lớn của embedding tables:
- Các đặc trưng categorical có mức độ quan trọng không đều
- Có thể áp dụng precision levels khác nhau cho từng nhóm

## 2. Phương pháp sử dụng

- Mixed-Precision Embeddings (MPE): Nhóm đặc trưng theo tần suất
- Gán precision levels phù hợp cho mỗi nhóm
- Học phân bố xác suất trên các mức precision
- Sampling strategy để xác định gán precision tối ưu

## 3. Thành tựu đạt được

- Nén embedding ~200x trên Criteo mà không giảm độ chính xác
- Vượt trội hơn các phương pháp nén hiện có trên 3 datasets

## 4. Hạn chế

- Vẫn under submission
- Không rõ chi phí tính toán search overhead
- Chỉ kiểm nghiệm trên 3 datasets
