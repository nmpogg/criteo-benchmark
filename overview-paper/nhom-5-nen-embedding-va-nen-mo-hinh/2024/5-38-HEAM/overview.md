# Review Paper: HEAM: Heterogeneous Memory Architecture for Proactive In-Memory Computing Embedding Acceleration

**ArXiv ID:** [2402.04032](https://arxiv.org/abs/2402.04032)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết nút thắt tính toán trong lớp embedding:
- Nén embedding tăng chi phí truy cập bộ nhớ và giao tiếp CPU-PIM

## 2. Phương pháp sử dụng

- Hệ thống PIM hai cấp: base-die PIM + bank-group PIM trong HBM
- Kiến trúc bộ nhớ dị hợp HBM-DIMM
- SRAM caching + subtable duplication
- Tối ưu cho weight-sharing (QR-trick, TT-Rec)

## 3. Thành tựu đạt được

- 2.22x tăng tốc trong QR-trick
- 2.15x tăng tốc trong TT-Rec

## 4. Hạn chế

- Chuyên biệt cho weight-sharing, hạn chế tính áp dụng rộng
- Overhead giao tiếp không thể hoàn toàn loại bỏ
