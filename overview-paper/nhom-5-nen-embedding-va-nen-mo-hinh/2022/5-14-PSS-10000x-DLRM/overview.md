# Review Paper: Trade-offs of Model Size: 10,000x Compressed DLRM Without Quality Losses

**ArXiv ID:** [2207.10731](https://arxiv.org/abs/2207.10731)
**Năm:** 2022 | **Venue:** NeurIPS 2022
**Tác giả:** Aditya Desai, Anshumali Shrivastava
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding tables chiếm 70-90% kích thước DLRM, lên tới hàng trăm GB với 25+ tỷ tham số. Điều này gây khó khăn lớn cho training và deployment (chậm, tốn tài nguyên phần cứng). Paper nghiên cứu cách **nén embedding tables cực mạnh** trong DLRM mà không làm giảm chất lượng dự đoán, sử dụng Criteo-TB dataset làm benchmark.

**Motivation:** Cần giảm kích thước model từ 100GB xuống mức có thể deploy trên thiết bị hạn chế tài nguyên, đồng thời cải thiện tốc độ inference.

## 2. Phương pháp sử dụng

**Parameter Sharing Setup (PSS):**
- Chia sẻ tham số embedding giữa các feature khác nhau thay vì mỗi feature có embedding riêng
- Chứng minh **giới hạn toán học (theoretical bounds)** rằng có thể dùng số lượng tham số exponentially ít hơn mà vẫn giữ độ chính xác trong khoảng (1±ε)
- Phương pháp không tạo sparsity → dễ deploy, không cần thay đổi infrastructure hay custom kernels
- Áp dụng trực tiếp lên bảng embedding hiện có

## 3. Thành tựu đạt được

| Metric | Kết quả |
|--------|---------|
| **Compression ratio** | 10,000× (100GB → 10MB) |
| **Accuracy** | Không mất chất lượng dự đoán trên Criteo-TB |
| **Training latency** | Cải thiện 4.3× nhờ giảm bộ nhớ |
| **Tổng thời gian training** | Giảm tổng thể (latency gain vượt qua slower convergence) |

Phương pháp production-ready, không yêu cầu thay đổi kiến trúc hệ thống.

## 4. Hạn chế

- **Convergence chậm:** Cần 4.5× nhiều iterations hơn để đạt saturation — trade-off giữa compression và tốc độ hội tụ
- **Chưa đánh giá inference:** Impact trên inference time thực tế chưa được phân tích chi tiết
- **Sharing conflicts:** Khi nhiều features chia sẻ cùng tham số, có thể xảy ra interference giữa các features không liên quan
