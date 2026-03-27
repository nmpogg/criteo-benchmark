# Review Paper: Enhancing CTR Prediction with De-correlated Expert Networks

**ArXiv ID:** [2505.17925](https://arxiv.org/abs/2505.17925)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo tập trung vào vấn đề mô hình hóa tương tác đặc trưng trong dự đoán CTR (Click-Through Rate). Mặc dù Mixture-of-Experts (MoE) được công nhận là cách tiếp cận hiệu quả để kết hợp nhiều chuyên gia trong dự đoán tương tác đặc trưng, các tác giả nhận thấy rằng hiệu quả thực tế của việc phân hóa các chuyên gia còn chưa rõ ràng. Vấn đề cơ bản là các chuyên gia trong MoE truyền thống có thể bị tương quan cao với nhau, giảm khả năng đa dạng hóa và độc lập của mô hình.

Động lực của nghiên cứu này là cần thiết phải cải thiện hiệu suất MoE bằng cách đảm bảo rằng các chuyên gia thực sự học các đặc trưng khác nhau, độc lập với nhau. Khoảng trống trong nghiên cứu hiện tại là thiếu một cơ chế rõ ràng để đo lường và giảm thiểu tương quan giữa các chuyên gia. Bài báo cũng xác định rằng các chiến lược khác nhau để giảm tương quan có thể bổ sung lẫn nhau, điều này chưa được khám phá đầy đủ.

## 2. Phương pháp sử dụng

Bài báo đề xuất framework D-MoE (De-Correlated Mixture-of-Experts) với cơ chế Cross-Expert De-Correlation loss. Kiến trúc chính bao gồm nhiều chuyên gia tương tác đặc trưng được kết hợp thông qua một gating mechanism, nhưng khác biệt chính là sự bổ sung của Cross-Expert De-Correlation loss để tối thiểu hóa tương quan giữa các đầu ra của chuyên gia.

Thành phần cốt lõi của D-MoE bao gồm:
- Các chuyên gia riêng lẻ học các tương tác đặc trưng
- Gating mechanism để cân bằng đóng góp của từng chuyên gia
- Cross-Expert De-Correlation loss để buộc các chuyên gia phải khác biệt với nhau

Kỹ thuật cốt lõi sử dụng một độ đo tương quan mới gọi là Cross-Expert Correlation metric, định lượng mức độ giảm tương quan giữa các chuyên gia. Tính mới về kỹ thuật nằm ở việc chứng minh rằng các chiến lược khác nhau để giảm tương quan là tương thích và tăng cường lẫn nhau, dần dần giảm tương quan và cải thiện hiệu suất mô hình.

## 3. Thành tựu đạt được

Kết quả thực nghiệm rộng rãi trên các tập dữ liệu công khai xác nhận hiệu quả của D-MoE. Đặc biệt, thử nghiệm A/B trên nền tảng quảng cáo của Tencent cho thấy kết quả sản xuất ấn tượng: mô hình đạt được mức nâng cao Gross Merchandise Volume (GMV) là **1.19%**. Đây là một cải thiện đáng kể khi triển khai trong môi trường sản xuất thực tế.

Ngoài các số liệu AUC và LogLoss cải thiện trên các tập dữ liệu offline, sự xác minh trực tiếp từ thử nghiệm sản xuất của Tencent cho thấy rằng việc giảm tương quan giữa các chuyên gia có tác động kinh tế tích cực rõ ràng. Sự tăng 1.19% GMV là bằng chứng mạnh mẽ cho hiệu quả thực tế của phương pháp.

## 4. Hạn chế

Một hạn chế tiềm ẩn của D-MoE là chi phí tính toán bổ sung từ việc tính toán Cross-Expert De-Correlation loss và đo lường tương quan giữa các chuyên gia. Bài báo không cung cấp phân tích chi tiết về độ phức tạp tính toán hoặc thời gian suy luận bổ sung.

Một hạn chế khác là khả năng tổng quát hóa của phương pháp chưa được kiểm chứng trên nhiều loại tập dữ liệu đa dạng (ví dụ: các nền tảng khác nhau, các lĩnh vực khác nhau ngoài quảng cáo). Đánh giá hiện tại chủ yếu dựa trên kết quả từ Tencent và các tập dữ liệu công khai, mà có thể không đủ để khẳng định tính cứng cáp của phương pháp trên các loại dữ liệu khác nhau trong thế giới thực.

Ngoài ra, bài báo chưa thảo luận chi tiết về cách chọn hợp lý số lượng chuyên gia hoặc cách điều chỉnh siêu tham số của Cross-Expert De-Correlation loss để đạt được cân bằng tối ưu giữa độ phân hóa của chuyên gia và hiệu suất tổng thể.
