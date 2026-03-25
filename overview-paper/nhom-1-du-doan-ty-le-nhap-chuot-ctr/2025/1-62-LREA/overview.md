# Review Paper: LREA: Low-Rank Efficient Attention on Modeling Long-Term User Behaviors for CTR Prediction

**ArXiv ID:** [2503.02542](https://arxiv.org/abs/2503.02542)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết challenge hiệu suất tính toán khi mô hình hóa user interest từ lịch sử hành vi dài:
- Cân bằng performance với response time requirements của production systems

## 2. Phương pháp sử dụng

- Low-rank matrix decomposition để tăng runtime performance
- Specialized loss function duy trì attention quality
- Matrix absorption và pre-storage techniques cho inference

## 3. Thành tựu đạt được

- Offline và online experiments: outperform state-of-the-art
- Cân bằng tốt giữa model performance và acceptable response times
- SIGIR 2025 Short Paper Track

## 4. Hạn chế

- Paper ngắn (5 trang)
- Traditional filtering methods bị mất mát thông tin đáng kể
- Hạn chế cụ thể của LREA không được chi tiết rõ
