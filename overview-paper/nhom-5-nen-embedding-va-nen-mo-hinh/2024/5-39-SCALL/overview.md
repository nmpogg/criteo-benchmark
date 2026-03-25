# Review Paper: SCALL: Scalable Dynamic Embedding Size Search for Streaming Recommendation

**ArXiv ID:** [2407.15411](https://arxiv.org/abs/2407.15411)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Thách thức lưu trữ trong streaming recommendation:
- Embedding phát triển liên tục, vượt quá giới hạn bộ nhớ

## 2. Phương pháp sử dụng

- Probabilistic sampling từ phân phối xác suất với budget định trước
- Adaptive adjustment tăng/giảm chiều embedding
- RL framework với mean pooling cho fixed-length state vectors
- Gán kích thước cho user/item chưa từng thấy

## 3. Thành tựu đạt được

- Hiệu quả vượt trội trên hai public datasets
- Được chấp nhận tại CIKM 2024

## 4. Hạn chế

- Chỉ đánh giá trên hai datasets
- Chưa kiểm chứng tăng trưởng cực đoan
