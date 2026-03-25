# Review Paper: MSD: Balancing Efficiency and Effectiveness - An LLM-Infused Approach for Optimized CTR Prediction

**ArXiv ID:** [2412.06860](https://arxiv.org/abs/2412.06860)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

CTR prediction cần nắm bắt thông tin ngữ nghĩa sâu sắc:
- Phương pháp truyền thống không mô hình hóa hiệu quả

## 2. Phương pháp sử dụng

- MSD (Multi-level Deep Semantic Information Infused CTR via Distillation)
- Dùng LLM trích xuất & chưng cất thông tin vào mô hình compact
- Kết hợp distillation để giữ hiệu suất, giảm chi phí

## 3. Thành tựu đạt được

- A/B test Meituan: vượt trội CPM & CTR so với baseline
- Cân bằng hiệu suất cao + tiêu thụ tài nguyên tối ưu

## 4. Hạn chế

- Không chi tiết thách thức kỹ thuật cụ thể
- Overhead chi phí LLM inference trong serving chưa rõ
