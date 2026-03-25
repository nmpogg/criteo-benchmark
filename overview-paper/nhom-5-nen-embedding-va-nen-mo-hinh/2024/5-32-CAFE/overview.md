# Review Paper: CAFE: Towards Compact, Adaptive, and Fast Embedding for Large-scale Recommendation Models (SIGMOD)

**ArXiv ID:** [2312.03256](https://arxiv.org/abs/2312.03256)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Ba mục tiêu cạnh tranh: hiệu quả bộ nhớ, latency thấp, thích ứng với phân phối động:
- Trong các mô hình khuyến nghị sâu

## 2. Phương pháp sử dụng

- Chiến lược nhiều tầng: đặc trưng quan trọng nhận embedding riêng, ít quan trọng chia sẻ qua hash
- HotSketch: cấu trúc dữ liệu nhận dạng đặc trưng có giá trị cao real-time
- Multi-level hash embedding tables

## 3. Thành tựu đạt được

- 10000x compression ratio trên Criteo
- AUC cao hơn 3.92% so với phương pháp nén hiện có
- Code công khai trên GitHub

## 4. Hạn chế

- Chưa rõ về độ phức tạp thời gian của HotSketch
- Giới hạn kiểm nghiệm chủ yếu trên Criteo family datasets
