# Review Paper: MLCC: Multi-Level Compression Cross Networks for Click-Through Rate Prediction

**ArXiv ID:** [2602.12041](https://arxiv.org/abs/2602.12041)
**Năm:** 2026
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Tối ưu hóa mô hình tương tác feature bậc cao cho prediction CTR/conversion trong hệ thống recommendation quy mô lớn:
- Làm sao tính toán các tương tác phức tạp giữa nhiều feature mà vẫn đạt hiệu suất cao
- Trong môi trường production có ràng buộc latency và tài nguyên tính toán

## 2. Phương pháp sử dụng

- Multi-Level Compression Cross Networks (MLCC): cấu trúc phân cấp để tổ chức feature crosses
- Dynamic Composition: kết hợp các cross khác nhau một cách linh hoạt
- Multi-Channel Extension (MC-MLCC): phân tách tương tác thành các subspace song song để scaling ngang
- Channel-based scaling như thay thế cho embedding inflation truyền thống
- A/B testing trên Bilibili advertising platform để xác thực thực tế

## 3. Thành tựu đạt được

- 0.52 AUC improvement so với DLRM-style baselines
- 26× reduction trong số parameters và computational operations mà vẫn bảo toàn performance
- Stable and predictable scaling behavior trên embedding dimension, head number, channel count
- Validation trên 3 public benchmarks + 1 proprietary dataset
- Triển khai thành công trong production environment (Bilibili)
- Giảm latency và resource consumption đáng kể

## 4. Hạn chế

- Đánh giá chủ yếu trên 4 datasets (3 public + 1 proprietary) - tính tổng quát hóa có thể bị hạn chế
- Thiết kế tối ưu cho môi trường production với ràng buộc strict - có thể không tổng quát cho các domain khác
- Thiếu ablation studies chi tiết
- Không so sánh chi tiết với các phương pháp compression embedding khác
