# Review Paper: Directed Acyclic Graph Factorization Machines for CTR Prediction via Knowledge Distillation

**ArXiv ID:** [2211.11159](https://arxiv.org/abs/2211.11159)
**Năm:** 2022
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cân bằng hiệu suất tính toán với độ chính xác mô hình khi triển khai hệ thống khuyến nghị quy mô công nghiệp

## 2. Phương pháp sử dụng

KD-DAGFM sử dụng knowledge distillation từ teacher phức tạp, cấu trúc DAG với dynamic programming

## 3. Thành tựu đạt được

Hiệu suất gần như không mất mát, giảm 78.5% chi phí tính toán (<21.5% FLOPs so với SOTA), xác thực trên 4 dataset (WeChat)

## 4. Hạn chế

Knowledge distillation không hoàn toàn bảo toàn hành vi teacher, mất mát thông tin từ compression chưa rõ
