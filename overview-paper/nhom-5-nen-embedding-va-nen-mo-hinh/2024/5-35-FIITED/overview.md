# Review Paper: FIITED: Fine-Grained Embedding Dimension Optimization During Training

**ArXiv ID:** [2401.04408](https://arxiv.org/abs/2401.04408)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Tối ưu hóa chiều embedding vector trong quá trình training:
- Các chiều vector embedding không đều nhau về tầm quan trọng
- Cho phép pruning có chọn lọc dựa trên tần suất và gradient

## 2. Phương pháp sử dụng

- FIITED: Điều chỉnh kích thước embedding thích ứng trong training
- Dựa trên tần suất đặc trưng và gradient importance
- Virtually-hashed physically-indexed hash tables cho pruning hiệu quả

## 3. Thành tựu đạt được

- Giảm kích thước embedding table 65%+ trên mô hình công nghiệp
- 2.1x đến 800x compression trên public datasets
- Cải thiện throughput đồng thời giảm bộ nhớ

## 4. Hạn chế

- Chưa rõ khả năng mở rộng trên kiến trúc DLRM khác nhau
- Hash tables complexity với feature sets cực lớn
