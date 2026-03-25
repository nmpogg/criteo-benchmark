# Review Paper: Single-shot Pruning for Rec Models via Shapley (Shaver)

**ArXiv ID:** [2411.13052](https://arxiv.org/abs/2411.13052)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Triển khai recommendation trên thiết bị tài nguyên hạn chế:
- Bảng embedding lớn là nút thắt lưu trữ

## 2. Phương pháp sử dụng

- Shaver: Shapley Value-guided Embedding Reduction
- Cooperative Game Theory để lượng hóa đóng góp mỗi tham số
- Field-aware codebook trong pruning giảm mất thông tin
- Single-shot, không cần retraining

## 3. Thành tựu đạt được

- Hiệu suất cạnh tranh trên nhiều budget tham số
- Một lần pruning không cần đắt đỏ retraining

## 4. Hạn chế

- Giới hạn trong content-based recommendation
- Chi tiết hạn chế chưa rõ
