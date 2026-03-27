# Review Paper: AdaS&S: Adaptive Shrinking & Splitting for Embedding Heterogeneity in Recommendation

**ArXiv ID:** [2411.07504](https://arxiv.org/abs/2411.07504)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Các phương pháp truyền thống sử dụng **kích thước embedding đồng nhất** cho tất cả features — gây lãng phí tài nguyên cho features đơn giản và thiếu capacity cho features phức tạp. Các phương pháp tự động tìm kiếm kích thước embedding hiện có gặp 3 thách thức: (1) kết quả tìm kiếm không ổn định, (2) hiệu suất không tối ưu, (3) chi phí bộ nhớ không kiểm soát được.

**Motivation:** Cần framework tự động xác định kích thước embedding tối ưu cho từng feature field, đảm bảo **ổn định** trong quá trình search và **cân bằng** giữa model performance với memory constraints.

## 2. Phương pháp sử dụng

**AdaS&S — 2 giai đoạn:**

1. **Giai đoạn 1 — Supernet Training:**
   - Sử dụng **Adaptive Sampling method** tách riêng việc train parameters và tìm kiếm kích thước
   - Tạo foundation supernet ổn định chứa các candidate embedding dimensions đa dạng
   - Giải quyết vấn đề training instability của các NAS approaches trước

2. **Giai đoạn 2 — RL-based Search:**
   - Sử dụng supernet đã train để tìm kiếm kích thước tối ưu
   - **Resource competition penalty:** Cơ chế phạt để cân bằng model performance với memory budget
   - RL agent học policy gán embedding dimensions cho từng field

## 3. Thành tựu đạt được

| Metric | Kết quả |
|--------|---------|
| **AUC improvement** | ~0.3% cải thiện |
| **Parameter reduction** | ~20% giảm tham số model |
| **Search stability** | Vượt trội so với các phương pháp cạnh tranh |

Giải quyết thách thức instability mà các NAS-based methods trước đây gặp phải.

## 4. Hạn chế

- **Modest AUC gain:** Cải thiện AUC 0.3% — incremental improvement
- **RL search cost:** Chi phí tính toán của giai đoạn RL-search chưa được công bố chi tiết
- **Limited datasets:** Chỉ đánh giá trên số lượng hạn chế recommendation datasets
- **Supernet sensitivity:** Tác động của kích thước supernet ban đầu không được thảo luận đầy đủ
- **Generalization:** Adaptive Sampling method cần được khái quát hóa thêm cho các loại model architectures khác
