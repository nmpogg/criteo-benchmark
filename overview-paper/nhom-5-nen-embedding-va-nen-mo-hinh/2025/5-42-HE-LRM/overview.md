# Review Paper: HE-LRM: Efficient Private Embedding Lookups for Neural Inference Using Fully Homomorphic Encryption

**ArXiv ID:** [2506.18150](https://arxiv.org/abs/2506.18150)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Thực hiện neural inference bảo vệ quyền riêng tư cho DLRMs:
- Embedding lookup mã hóa trên bảng embedding lớn sử dụng FHE
- FHE có các toán tử tính toán hạn chế

## 2. Phương pháp sử dụng

- Nén embedding phía client sử dụng digit decomposition
- Packing multi-embedding cho phép lookups song song trên nhiều bảng
- Tối ưu hóa để tương thích với tính toán mã hóa downstream

## 3. Thành tựu đạt được

- Đạt 56× speedup so với state-of-the-art
- End-to-end encrypted DLRM inference trên dataset benchmark
- Latency: 24s (UCI health), 489s (Criteo click-prediction)

## 4. Hạn chế

- Latency vẫn quá lớn cho deployment thực tế
- Phạm vi đánh giá chủ yếu là DLRM
- Bị hạn chế bởi các toán tử tính toán của FHE
