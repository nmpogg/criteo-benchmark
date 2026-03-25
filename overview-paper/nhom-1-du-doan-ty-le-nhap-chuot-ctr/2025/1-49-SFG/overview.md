# Review Paper: From Feature Interaction to Feature Generation: A Generative Paradigm of CTR Prediction Models

**ArXiv ID:** [2512.14041](https://arxiv.org/abs/2512.14041)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết giới hạn của các mô hình CTR phân biệt hiện tại:
- Nhận dạng vấn đề "embedding dimensional collapse" và thừa dư thông tin
- Đề xuất chuyển từ paradigm tương tác sang phát sinh đặc trưng

## 2. Phương pháp sử dụng

- Framework Supervised Feature Generation (SFG) với hai thành phần:
  - Encoder: xây dựng embedding ẩn cho đặc trưng
  - Decoder: tái tạo embedding đặc trưng từ biểu diễn ẩn
- Sử dụng loss signal có giám sát thay vì self-supervised
- Tương thích với các mô hình CTR hiện tại

## 3. Thành tựu đạt được

- Giảm thiểu embedding collapse, giảm thừa dư thông tin
- Cải thiện hiệu suất nhất quán trên nhiều tập dữ liệu và mô hình cơ sở
- Code công khai trên GitHub (GE4Rec repository)

## 4. Hạn chế

- Chưa chi tiết về chi phí tính toán, độ phức tạp mở rộng
- Không rõ các tình huống mô hình có thể không hoạt động tốt
- Độ cải thiện cụ thể trên các dataset khác nhau không được cung cấp
