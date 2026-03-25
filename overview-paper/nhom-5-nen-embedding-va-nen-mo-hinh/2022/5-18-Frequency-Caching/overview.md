# Review Paper: Frequency-aware Caching for Embedding Tables in Large-scale Recommendation Models

**ArXiv ID:** [2208.05321](https://arxiv.org/abs/2208.05321)
**Năm:** 2022
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Quản lý bảng embedding không vừa GPU memory, dùng frequency statistics

## 2. Phương pháp sử dụng

Frequency-aware software cache, dynamic management giữa CPU-GPU, hybrid parallel training

## 3. Thành tựu đạt được

Giữ chỉ 1.5% embedding parameters trên GPU vẫn đạt decent training speed

## 4. Hạn chế

Phụ thuộc phân bố tần suất bị lệch, lợi ích phụ thuộc dataset
