# Review Paper: Memory Efficient Mixed-Precision Optimizers

**ArXiv ID:** [2309.12381](https://arxiv.org/abs/2309.12381)
**Năm:** 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giảm tiêu thụ bộ nhớ khi huấn luyện neural network bằng tối ưu floating-point arithmetic

## 2. Phương pháp sử dụng

Loại bỏ bản sao single-precision, kết hợp single và half-precision, tích hợp optimizer vào backpropagation

## 3. Thành tựu đạt được

Giảm 25% memory peak, tăng tốc 15%, duy trì accuracy

## 4. Hạn chế

Không rõ loại mô hình hưởng lợi nhất, thiếu thông tin scalability
