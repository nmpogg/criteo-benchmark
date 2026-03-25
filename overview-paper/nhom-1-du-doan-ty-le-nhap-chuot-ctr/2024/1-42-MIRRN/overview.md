# Review Paper: MIRRN: Multi-granularity Interest Retrieval and Refinement Network for Long-Term User Behavior Modeling in CTR

**ArXiv ID:** [2411.15005](https://arxiv.org/abs/2411.15005)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện mô hình hóa hành vi người dùng dài hạn trong CTR:
- Phương pháp chỉ dựa thông tin mục tiêu bỏ qua đa dạng lợi ích
- Bỏ qua mối quan hệ tuần tự, tương tác

## 2. Phương pháp sử dụng

- Xây dựng truy vấn từ hành vi ở khoảng thời gian khác nhau (multi-granularity)
- Multi-head Fourier transformer học thông tin tuần tự & tương tác
- Multi-head target attention đánh giá tác động lợi ích

## 3. Thành tựu đạt được

- Vượt trội SOTA trong thử nghiệm
- A/B test Huawei Music: +1.32% bài hát nghe, +0.55% thời gian nghe
- Code công khai

## 4. Hạn chế

- Không thảo luận chi tiết hạn chế
