# Review Paper: EVStore: Storage and Caching Capabilities for Scaling Embedding Tables in Deep Recommendation Systems

**ArXiv ID:** [ACM 10.1145/3575693.3575718](https://arxiv.org/abs/ACM 10.1145/3575693.3575718)
**Năm:** 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Lưu trữ bảng embedding ngày càng lớn trong bộ nhớ, mỗi inference cần nhiều lookups. ASPLOS 2023

## 2. Phương pháp sử dụng

Hệ thống 3 lớp EVStore, tận dụng structural regularity, domain-specific approximations, optimized caching

## 3. Thành tựu đạt được

Giảm 23% avg latency, 27% p90 latency, 4x throughput, 94% memory reduction, chỉ 0.2% accuracy loss

## 4. Hạn chế

0.2% accuracy loss cho ứng dụng sensitive, phụ thuộc structural regularity
