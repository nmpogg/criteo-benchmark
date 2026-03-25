# Review Paper: Mutual Learning for Finetuning Click-Through Rate Prediction Models

**ArXiv ID:** [2406.12087](https://arxiv.org/abs/2406.12087)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện mô hình CTR bằng mutual learning thay vì knowledge distillation truyền thống:
- Mô hình CTR thường không có sự chênh lệch hiệu suất lớn
- Knowledge distillation kém hiệu quả khi mô hình cân bằng

## 2. Phương pháp sử dụng

- Mutual learning algorithms: huấn luyện cộng tác các mô hình tương tự
- Các mô hình có độ phức tạp ngang bằng học từ nhau đồng thời
- Đánh giá trên Criteo và Avazu datasets

## 3. Thành tựu đạt được

- Chứng minh mutual learning hiệu quả hơn khi mô hình cân bằng
- ~0.66% relative improvement
- Phương pháp đơn giản, dễ triển khai

## 4. Hạn chế

- Báo cáo ngắn (7 trang)
- Không rõ khả năng mở rộng, chi phí tính toán
- Thiếu lý giải lý thuyết
