# Review Paper: SparseCTR: Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction

**ArXiv ID:** [2601.17836](https://arxiv.org/abs/2601.17836)
**Năm:** 2026
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Phát triển cơ chế attention hiệu quả để giải quyết thách thức triển khai trong hệ thống recommendation:
- Tập trung xử lý long-term user behaviors với sparse attention
- Mục tiêu: giảm computational cost mà vẫn duy trì/cải thiện hiệu suất

## 2. Phương pháp sử dụng

Sparse Attention Mechanism với 3 thành phần chính:
- Personalized Chunking: Phân chia behavior sequences theo cách riêng từng user để bảo tồn continuous patterns và cho phép parallel processing
- Three-Branch Sparse Attention: Bắt giữ 3 khía cạnh: global user interests, interest transitions, short-term interests
- Composite Relative Temporal Encoding: Sử dụng learnable head-specific bias coefficients để biểu diễn sequential và periodic relationships

## 3. Thành tựu đạt được

- Cải thiện computational efficiency với kết quả superior vs methods hiện tại
- Scaling law consistency: Lợi ích scaling đều đặn qua 3 orders of magnitude trong FLOPs
- Online A/B testing results:
  - CTR improvement: +1.72%
  - CPM improvement: +1.41%
- Accepted to WWW 2026

## 4. Hạn chế

- Personalized chunking có thể gặp khó khăn với user behavior patterns không rõ ràng
- Phức tạp triển khai hệ thống chunking per-user trong production
- Khả năng generalization trên các domain khác chưa được kiểm chứng
