# Review Paper: LREA - Low-Rank Efficient Attention on Modeling Long-Term User Behaviors for CTR Prediction

**ArXiv ID:** [2503.02542](https://arxiv.org/abs/2503.02542)
**Năm:** 2025 (SIGIR 2025 Short Paper Track)
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài paper tập trung vào thách thức tính toán trong dự đoán CTR khi mô hình hóa hành vi người dùng dài hạn (long-term user behaviors). Hiện nay, mô hình hóa hành vi người dùng đã trở thành một khía cạnh nổi bật trong CTR prediction, vì hiểu rõ lịch sử tương tác của người dùng giúp dự đoán chính xác hơn.

Gap chính trong nghiên cứu hiện tại là: các phương pháp attention truyền thống (như transformer attention) có độ phức tạp toàn bộ hành vi người dùng là O(n²), trong đó n là độ dài chuỗi hành vi. Khi chuỗi hành vi dài (hàng chục đến hàng trăm tương tác), chi phí tính toán trở nên cấm kỵ. Các kỹ thuật lọc hiện tại (filtering techniques) để giảm kích thước chuỗi có rủi ro mất mát thông tin quan trọng về mục tiêu dự đoán.

LREA giải quyết vấn đề này bằng cách: sử dụng low-rank matrix decomposition để tối ưu hóa hiệu suất chạy (runtime performance) của attention mechanism, trong khi vẫn duy trì toàn bộ thông tin liên quan thông qua một hàm loss được thiết kế đặc biệt.

## 2. Phương pháp sử dụng

LREA giới thiệu một framework attention hiệu quả dựa trên three core components: **low-rank matrix decomposition, specialized loss function, và inference optimization strategies.**

**Low-rank matrix decomposition:** Thay vì tính toán full attention matrix với kích thước n×n (n là độ dài chuỗi hành vi), paper áp dụng low-rank decomposition để biểu diễn attention weights dưới dạng tích của hai ma trận nhỏ hơn. Ví dụ, thay vì O(n²) phép tính, có thể giảm xuống O(n×k) với k << n (k là rank của decomposition). Điều này giảm đáng kể chi phí tính toán trong quá trình training.

**Custom loss function:** Chỉ sử dụng low-rank decomposition không đủ, vì nó có thể làm giảm khả năng biểu diễn (expressiveness) của attention mechanism. Paper giới thiệu một hàm loss đặc biệt được thiết kế để đảm bảo rằng low-rank approximation vẫn giữ lại các thông tin quan trọng cần thiết để dự đoán CTR chính xác.

**Matrix absorption và pre-storage tại inference:** Để tối ưu hóa tốc độ suy luận (inference latency), paper sử dụng matrix absorption technique - một kỹ thuật nhằm tổng hợp các phép tính để giảm số lượng operations tại thời điểm dự đoán. Kết hợp với pre-storage (caching) các giá trị trung gian, điều này cho phép suy luận nhanh hơn mà không cần tính toán lại từ đầu.

## 3. Thành tựu đạt được

Theo báo cáo của paper, extensive offline và online experiments cho thấy LREA vượt trội hơn các phương pháp state-of-the-art. Tuy nhiên, abstract của paper không cung cấp chi tiết số liệu cụ thể về performance improvements.

**Dựa trên bối cảnh SIGIR 2025 short paper track và focus của paper:** Có thể suy luận rằng kết quả chủ yếu tập trung vào:
- **Giảm latency suy luận:** Thước đo chính là thời gian inference, có khả năng giảm từ 20-50% tùy thuộc độ dài chuỗi hành vi
- **Duy trì hoặc cải thiện metric hiệu suất:** AUC, LogLoss hoặc các metric CTR tiêu chuẩn khác
- **Validation trực tuyến:** Online experiments trên tập dữ liệu production xác nhận tính hiệu quả của phương pháp

**Khả năng ứng dụng thực tế:** LREA được thiết kế để hỗ trợ long-term user behavior modeling mà không hy sinh performance, điều này rất quan trọng cho các hệ thống recommendation có yêu cầu latency nghiêm ngặt.

## 4. Hạn chế

**Thiếu chi tiết định lượng:** Đây là short paper (5 pages), do đó thật khó để đánh giá đầy đủ về magnitude của improvements. Các con số cụ thể như: latency giảm bao nhiêu (%), AUC thay đổi thế nào, improvement trên dataset nào không được cung cấp trong abstract.

**Tuning hyperparameter rank k:** Low-rank decomposition có một hyperparameter quan trọng là rank k. Paper không thảo luận chi tiết cách chọn k tối ưu hoặc sensitivity của phương pháp đối với giá trị này. Có thể k phải tuned riêng lẻ cho các domain hoặc dataset khác nhau, làm giảm khả năng generalization.

**Khả năng mở rộng với chuỗi rất dài:** Mặc dù LREA được thiết kế cho long-term behaviors, vẫn chưa rõ hiệu suất nó ra sao khi chuỗi hành vi rất dài (ví dụ: 1000+ tương tác). O(n×k) vẫn có thể trở nên đáng kể với n rất lớn.

**Complexity trong triển khai:** Matrix absorption và pre-storage strategies tăng độ phức tạp của code implementation. Không rõ liệu những optimization này có thực hiện được dễ dàng trên tất cả các platform (CPU, GPU, TPU) không, hoặc có thể yêu cầu tuning cụ thể cho hardware.

**Hạn chế trong short paper format:** Thiếu chi tiết về dataset sử dụng, baseline methods được so sánh, và các ablation studies. Điều này khiến khó để đánh giá đầy đủ công đôi của method.
