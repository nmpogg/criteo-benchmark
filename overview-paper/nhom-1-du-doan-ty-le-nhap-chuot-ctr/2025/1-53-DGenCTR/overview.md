# Review Paper: DGenCTR: Towards a Universal Generative Paradigm for CTR Prediction via Discrete Diffusion

**ArXiv ID:** [2508.14500](https://arxiv.org/abs/2508.14500)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Xử lý CTR prediction bằng cách tiếp cận generative:
- Phát triển framework cụ thể cho CTR thay vì sử dụng phương pháp tạo chuỗi
- Bảo tồn các tương tác cross-feature quan trọng

## 2. Phương pháp sử dụng

- Hai giai đoạn:
  - Pre-training generative dựa trên discrete diffusion
  - Fine-tuning có giám sát hướng tới CTR
- Hoạt động ở mức mẫu chứ không phải tạo các mục riêng lẻ

## 3. Thành tựu đạt được

- Xác thực thông qua cả thí nghiệm offline lẫn A/B testing trực tuyến
- Chứng minh hiệu quả trong các ứng dụng thực tế

## 4. Hạn chế

- Chưa chi tiết các hạn chế cụ thể
- Bài báo tương đối ngắn (11 trang)
- Khả năng tổng quát hóa trên các datasets đa dạng chưa rõ
