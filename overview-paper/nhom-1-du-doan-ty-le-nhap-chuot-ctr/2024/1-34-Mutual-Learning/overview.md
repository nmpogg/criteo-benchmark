# Review Paper: Mutual Learning for Finetuning Click-Through Rate Prediction Models

**ArXiv ID:** [2406.12087](https://arxiv.org/abs/2406.12087)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo lập luận rằng **Knowledge Distillation (KD) không hiệu quả cho CTR models** vì khoảng cách hiệu suất giữa teacher và student quá nhỏ. Trong CTR prediction, các mô hình phức tạp và đơn giản thường có performance gần nhau — không có teacher "giỏi hơn nhiều" để distill. Thay vì paradigm teacher-student truyền thống, tác giả đề xuất **mutual learning** — nhiều mô hình có khả năng tương đương học hỏi từ nhau đồng thời.

## 2. Phương pháp sử dụng

**Mutual Learning Framework:**

- Huấn luyện **song song nhiều mô hình cùng kích thước** nhưng khác về initialization hoặc hyperparameters
- Các mô hình **chia sẻ gradient/loss từ nhau** để tối ưu hóa — peer-to-peer thay vì top-down
- Không cần kiến trúc khác biệt đáng kể giữa các mô hình — tất cả đều là "peers" bình đẳng
- Phương pháp đơn giản, dễ triển khai — không cần pre-train teacher model trước
- Đánh giá trên Criteo và Avazu datasets

## 3. Thành tựu đạt được

- Chứng minh mutual learning hiệu quả hơn KD khi models cân bằng
- Cải thiện **~0.66% relative improvement** so với baselines
- Phương pháp đơn giản, dễ tích hợp vào existing training pipelines
- Kết quả nhất quán trên các CTR models phổ biến

## 4. Hạn chế

- Bài báo ngắn (**7 trang**) — thiếu khám phá sâu về khi nào mutual learning vượt trội
- Mức cải thiện **0.66% khiêm tốn** — không chắc significant trong production systems
- Chi phí memory **gấp đôi** do phải giữ nhiều models trong training
- Thiếu so sánh với các techniques khác (mixup, regularization, data augmentation)
- Thiếu lý giải lý thuyết vì sao mutual learning hoạt động tốt hơn
