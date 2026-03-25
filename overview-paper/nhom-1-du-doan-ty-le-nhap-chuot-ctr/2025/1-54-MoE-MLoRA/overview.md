# Review Paper: MoE-MLoRA for Multi-Domain CTR Prediction: Efficient Adaptation with Expert Specialization

**ArXiv ID:** [2506.07563](https://arxiv.org/abs/2506.07563)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết thách thức cá nhân hóa hệ thống khuyến nghị trên nhiều lĩnh vực (multi-domain):
- Các phương pháp truyền thống chỉ áp dụng một adaptation duy nhất trên mỗi domain
- Thiếu linh hoạt cho các mô hình tương tác đa dạng

## 2. Phương pháp sử dụng

- Mixture-of-Experts (MoE) framework với experts chuyên biệt độc lập trong domain riêng
- Gating network để động học trọng số đóng góp từ từng expert
- LoRA (Low-Rank Adaptation) cho hiệu quả tham số

## 3. Thành tựu đạt được

- Kiểm tra trên 8 CTR models với datasets Movielens & Taobao
- +1.45 Weighted-AUC improvement trên Taobao-20
- Chứng minh task-aware specialization & adaptive gating tăng độ chính xác

## 4. Hạn chế

- Lợi ích tối thiểu trên datasets có độ diversity & sparsity thấp
- Larger expert ensembles không cải thiện liên tục hiệu suất
- Cần careful model-specific tuning cho mỗi trường hợp
