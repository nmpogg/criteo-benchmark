# Review Paper: HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction

**ArXiv ID:** [2601.12681](https://arxiv.org/abs/2601.12681)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết bài toán xử lý đồng thời dữ liệu sequence người dùng dài và các đặc trưng không-sequence trong hệ thống recommendation công nghiệp:
- Các phương pháp truyền thống tách biệt xử lý sequence modeling và feature interaction một cách tuần tự
- Mục tiêu: kết hợp cả hai tác vụ hiệu quả dưới các ràng buộc tính toán

## 2. Phương pháp sử dụng

Hybrid Transformer (HyFormer):
- Query Decoding: Mở rộng đặc trưng không-sequence thành Global Tokens và decode sequences dài bằng key-value representations theo từng layer
- Query Boosting: Tăng cường cross-query và cross-sequence interactions thông qua efficient token mixing
- Cơ chế lặp lại qua các layers để tinh chỉnh semantic representations từng bước

## 3. Thành tựu đạt được

- Vượt trội so với baseline LONGER và RankMixer với budget tính toán tương đương
- Khả năng scaling tốt khi tăng parameters và computational operations
- Kiểm chứng online: A/B testing trong hệ thống production có traffic cao
- Cải thiện đáng kể so với các mô hình state-of-the-art đang được triển khai

## 4. Hạn chế

- Không nêu rõ cụ thể đơn vị/phần trăm cải thiện
- Độ phức tạp của hybrid architecture có thể làm khó khăn cho việc maintain
- Chi phí training có thể cao do chuỗi lặp qua layers
