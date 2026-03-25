# Review Paper: GAP-Net — Calibrating User Intent via Gated Adaptive Progressive Learning for CTR Prediction

**ArXiv:** [2601.07613](https://arxiv.org/abs/2601.07613) | **Năm:** 2026
**Tác giả:** Shenqiang Ke, Jianxiong Wei, Qingsong Hua

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **sequential user behavior modeling cho CTR prediction**, tập trung giải quyết ba vấn đề cụ thể mà các attention-based models hiện tại gặp phải:

- **Attention Sink:** Cơ chế attention truyền thống phân bổ probability mass không hợp lý — tập trung vào các behaviors nhiễu (noisy) thay vì các behaviors thực sự có giá trị. Ví dụ, một click ngẫu nhiên vào quảng cáo có thể nhận attention weight cao hơn cả chuỗi hành vi mua sắm có chủ đích.
- **Static Query Assumption:** Các mô hình giả định intent của user là cố định trong suốt sequence, bỏ qua thực tế là ý định thay đổi liên tục (dynamic intent shifts). User có thể bắt đầu phiên tìm kiếm điện thoại nhưng dần chuyển sang phụ kiện.
- **Rigid View Aggregation:** Khi tổng hợp tín hiệu từ nhiều nguồn (multi-view), các mô hình sử dụng trọng số cố định, không thích ứng linh hoạt với tầm quan trọng thay đổi theo thời gian của từng loại tín hiệu.

## 2. Phương pháp sử dụng

**GAP-Net — Triple Gating Architecture** với thiết kế phân cấp 3 tầng (micro → meso → macro):

**Tầng Micro — Adaptive Sparse-Gated Attention (ASGA):**
- Enforce sparsity ở cấp độ attention weights để loại bỏ noise
- Thay vì soft attention (mọi behaviors đều nhận weight > 0), ASGA chủ động đặt weight = 0 cho behaviors không liên quan
- Giải quyết trực tiếp vấn đề Attention Sink

**Tầng Meso — Gated Cascading Query Calibration (GCQC):**
- Dynamically cập nhật query vector qua cascading gates kết nối real-time triggers với long-term memories
- Query không còn static — mà được calibrate liên tục dựa trên context hiện tại
- Giải quyết vấn đề Static Query Assumption

**Tầng Macro — Context-Gated Denoising Fusion (CGDF):**
- Modulation ở mức multi-view aggregation: tự động điều chỉnh trọng số cho từng view (short-term, long-term, context) dựa trên tín hiệu ngữ cảnh
- Denoising mechanism loại bỏ thêm noise ở mức tổng hợp cuối cùng
- Giải quyết vấn đề Rigid View Aggregation

**Triết lý thiết kế:** Progressive refinement — thông tin được lọc và tinh chỉnh dần qua 3 tầng, từ chi tiết nhất (micro) đến tổng quát nhất (macro).

## 3. Thành tựu đạt được

- **Cải thiện đáng kể** so với state-of-the-art baselines trên industrial datasets
- **Robustness vượt trội** chống interaction noise và intent drift — mô hình duy trì hiệu suất khi dữ liệu nhiễu hoặc ý định user thay đổi nhanh
- **Kiến trúc có tính giải thích:** 3 tầng gating tương ứng 3 vấn đề cụ thể, dễ phân tích đóng góp từng thành phần (ablation study)
- **Paper 9 trang, 3 figures** — trình bày ngắn gọn, tập trung

## 4. Hạn chế

- **Thiếu metrics định lượng cụ thể** trong abstract: không báo cáo AUC, LogLoss, hay improvement percentages
- **Độ phức tạp kiến trúc:** Triple gating (3 tầng × mỗi tầng có gating mechanism riêng) tăng số lượng hyperparameters cần tune và tăng inference latency
- **Chưa có online A/B testing results** — chỉ đánh giá trên industrial datasets offline
- **Chưa so sánh chi phí tính toán** với các baselines đơn giản hơn (FLOPs, latency, memory)
- **Chưa rõ industrial datasets nào** được sử dụng — khó reproduce kết quả
