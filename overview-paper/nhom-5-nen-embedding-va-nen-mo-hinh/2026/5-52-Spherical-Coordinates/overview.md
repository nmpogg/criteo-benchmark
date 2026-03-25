# Review Paper: Embedding Compression via Spherical Coordinates

**ArXiv ID:** [2602.00079](https://arxiv.org/abs/2602.00079)
**Năm:** 2026
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Nén lossless các vector nhúng có chuẩn đơn vị (unit-norm embeddings):
- Loại dữ liệu thường dùng trong xử lý văn bản, ảnh và các tác vụ multi-vector
- Tận dụng tính chất hình học: tọa độ cầu của vector đơn vị chiều cao tập trung xung quanh π/2
- Dẫn đến sự suy thoái của số mũ floating-point và các bit mantissa theo mô hình dự đoán được

## 2. Phương pháp sử dụng

- Phân tích tính chất hình học của vector đơn vị trong không gian chiều cao
- Quantize tọa độ cầu (spherical coordinates) nhờ nhận thấy giá trị tập trung
- Áp dụng entropy coding cho các exponent và mantissa bits
- Kiểm thử trên 26 cấu hình khác nhau với các loại embedding khác nhau

## 3. Thành tựu đạt được

- 1.5× compression ratio - tốt hơn 25% so với phương pháp lossless tốt nhất trước đó
- Sai số tái tạo cực nhỏ (<1e-7), dưới machine epsilon của float32
- Hiệu quả nhất quán trên nhiều loại embedding (text, image, multi-vector)
- Được chấp nhận tại ICLR 2026 Workshop on Geometry-grounded Representation Learning

## 4. Hạn chế

- Chuyên biệt cho vector nhúng có chuẩn đơn vị - không áp dụng cho vector không được chuẩn hóa
- Không có thảo luận chi tiết về các trường hợp suy thoái (edge cases)
- Chưa được đánh giá trên các tác vụ CTR/recommendation cụ thể (chỉ là compression cho embeddings nói chung)
