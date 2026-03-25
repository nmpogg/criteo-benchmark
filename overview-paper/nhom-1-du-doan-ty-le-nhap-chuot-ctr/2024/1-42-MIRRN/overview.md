# Review Paper: MIRRN: Multi-granularity Interest Retrieval and Refinement Network for Long-Term User Behavior Modeling in CTR

**ArXiv ID:** [2411.15005](https://arxiv.org/abs/2411.15005)
**Năm:** 2024 | **Deployed:** Huawei Music App
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết 2 hạn chế trong mô hình hóa hành vi dài hạn. (1) Truy vấn chỉ dựa thông tin target item → **không nắm bắt đa dạng interests** — user có nhiều sở thích khác nhau, không chỉ liên quan item hiện tại. (2) Models bỏ qua **sequential patterns và inter-relationships** giữa các sub-sequences hành vi. Vấn đề đặc biệt quan trọng trong music streaming nơi interests thay đổi theo thời gian và ngữ cảnh.

## 2. Phương pháp sử dụng

**MIRRN** hoạt động qua 3 giai đoạn:

- **Multi-granularity Retrieval**: Xây dựng truy vấn từ behaviors ở **nhiều mức thời gian khác nhau** (recent, weekly, monthly) → retrieve sub-sequences nắm bắt interests ở các cấp độ khác nhau
- **Sequential Learning**: Áp dụng **Multi-head Fourier Transformer** để trích xuất sequential patterns và interactions trong sub-sequences — Fourier giúp mô hình hóa periodic patterns hiệu quả
- **Adaptive Refinement**: Sử dụng **Multi-head Target Attention** để cân nhắc ảnh hưởng của multi-granularity interests lên target item → weighted prediction

## 3. Thành tựu đạt được

- Vượt trội SOTA trong offline experiments
- **A/B test trên Huawei Music App**: **+1.32%** bài hát nghe, **+0.55%** thời gian nghe — significant cho music streaming
- Code công khai cho reproducibility
- Deployed production tại Huawei

## 4. Hạn chế

- Offline metrics cụ thể (AUC, CTR lift) trên public datasets không công bố
- Chi phí Multi-head Fourier Transformer không được so sánh chi tiết
- Sensitivity với hyperparameters (sub-sequence lengths, granularity levels) chưa phân tích
- Generalization sang domains khác ngoài music chưa đánh giá
