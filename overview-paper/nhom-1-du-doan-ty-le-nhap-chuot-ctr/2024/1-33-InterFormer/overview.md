# Review Paper: InterFormer: Effective Heterogeneous Interaction Learning for CTR Prediction

**ArXiv ID:** [2411.09852](https://arxiv.org/abs/2411.09852)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

InterFormer giải quyết hai vấn đề cốt lõi trong tích hợp dữ liệu heterogeneous cho CTR prediction. Thứ nhất, lưu lượng thông tin giữa các data modes (user profiles, behavior sequences, item features) là **unidirectional** — thông tin chỉ chảy một chiều, dẫn đến tương tác inter-mode không đủ. Thứ hai, **early aggregation** các nguồn dữ liệu heterogeneous gây mất thông tin nghiêm trọng — khi kết hợp sớm, chi tiết quan trọng từ từng mode bị loại bỏ trước khi model có cơ hội học tương tác phức tạp.

## 2. Phương pháp sử dụng

**InterFormer module:**

- **Bidirectional information flow**: Cho phép trao đổi thông tin hai chiều giữa các data modes — mỗi mode vừa gửi vừa nhận thông tin từ modes khác
- **Separate bridging architecture**: Thay vì aggregate sớm, duy trì thông tin đầy đủ trong mỗi mode, sử dụng "cầu nối" riêng biệt để lựa chọn và tóm tắt thông tin hiệu quả
- **Modified Transformer**: Hỗ trợ tương tác đa hướng, cho phép mỗi mode trích xuất thông tin liên quan từ modes khác mà không mất dữ liệu
- Thiết kế bởi 28 tác giả từ hợp tác công nghiệp lớn — focus vào tính thực tiễn

## 3. Thành tựu đạt được

- **SOTA trên 3 public datasets + 1 industrial-scale dataset**
- Giải quyết inter-mode interaction không đủ và information loss từ early aggregation
- 28 tác giả từ các tổ chức công nghiệp lớn — chứng minh giá trị triển khai thực tế
- Cải tiến đáng kể so với CTR methods hiện tại

## 4. Hạn chế

- Chi phí tính toán của bidirectional information exchange liên tục giữa modes chưa phân tích
- Scalability trên datasets cực lớn với nhiều data modes chưa kiểm chứng
- Thiếu so sánh trade-off giữa interaction depth và inference latency
- Chi tiết kiến trúc bridging arch chưa làm rõ đầy đủ trong abstract
