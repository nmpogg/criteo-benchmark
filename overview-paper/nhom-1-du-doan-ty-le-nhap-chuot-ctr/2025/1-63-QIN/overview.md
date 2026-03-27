# Review Paper: Quadratic Interest Network for Multimodal Click-Through Rate Prediction

**ArXiv ID:** [2504.17699](https://arxiv.org/abs/2504.17699)
**Năm:** 2025 (WWW 2025 EReL@MIR Workshop)
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài paper tập trung vào dự đoán CTR trong bối cảnh multimodal (đa phương thức), nơi dữ liệu bao gồm nhiều loại khác nhau: văn bản (text), hình ảnh (images), và nhật ký hành vi (behavioral logs). Đây là một bước tiến so với các mô hình CTR truyền thống chỉ xử lý tính năng bảng (tabular features).

Vấn đề chính mà paper giải quyết là: **cân bằng giữa semantic richness (độ phong phú semantic) từ dữ liệu đa phương thức và ràng buộc real-time inference trong production environments.** Dữ liệu multimodal cung cấp thông tin phong phú hơn về người dùng và item, nhưng việc xử lý các dữ liệu này (đặc biệt là hình ảnh) trong neural networks yêu cầu chi phí tính toán lớn. Đối với các hệ thống real-time recommendation, latency chỉ dưới vài trăm milliseconds, nên không thể sử dụng các mô hình quá phức tạp.

QIN (Quadratic Interest Network) được đề xuất như một giải pháp để: (1) khai thác thông tin từ đa phương thức hiệu quả, (2) mô hình hóa các tương tác tính năng high-order (bậc cao), (3) vẫn duy trì latency chấp nhận được để triển khai production.

## 2. Phương pháp sử dụng

QIN bao gồm hai thành phần cốt lõi hoạt động synergistically để xử lý dữ liệu multimodal:

**Adaptive Sparse Target Attention:** Thành phần này được thiết kế để trích xuất các mẫu hành vi người dùng từ dữ liệu multimodal một cách hiệu quả. Thay vì tính attention giữa tất cả các cặp phần tử (full attention), adaptive sparse target attention tập trung vào một subset các phần tử quan trọng nhất liên quan đến item được dự đoán (target). "Adaptive" có nghĩa là mô hình tự động học cách chọn lựa phần tử nào quan trọng, thay vì sử dụng heuristics cố định. "Sparse" có nghĩa là chỉ tính attention cho một vài phần tử đã chọn, giảm chi phí tính toán so với full attention O(n²) xuống O(n×s) với s << n.

**Quadratic Neural Networks:** Để mô hình hóa các tương tác tính năng bậc cao (high-order feature interactions), QIN sử dụng Quadratic Neural Networks thay vì các fully-connected layers truyền thống. Quadratic networks mô hình hóa các tương tác bậc 2 giữa các tính năng, nghĩa là chúng học được cách các cặp tính năng tương tác với nhau. Ví dụ: mô hình có thể học được rằng sự kết hợp giữa "người dùng nữ" + "item thời trang" có tương tác mạnh, trong khi "người dùng nam" + "item thời trang" có tương tác yếu hơn.

**Tích hợp trong kiến trúc:** Adaptive sparse target attention trích xuất thông tin multimodal liên quan và tạo ra các representation của hành vi người dùng, sau đó được đưa vào Quadratic Neural Networks để tính toán dự đoán CTR. Cách thiết kế này cân bằng tính toán: attention giảm chi phí bằng sparsity, quadratic networks xử lý feature interactions hiệu quả hơn fully-connected layers.

## 3. Thành tựu đạt được

**Leaderboard Performance - AUC: 0.9798** - Đây là một điểm số rất cao cho task dự đoán CTR. AUC (Area Under the Curve) của 0.9798 có nghĩa là mô hình có khả năng phân biệt giữa items sẽ bị click và không bị click với độ chính xác gần 98%. Để có perspective: AUC > 0.95 được coi là excellent, vì vậy 0.9798 nằm trong top tier của hiệu suất.

**Competition Standing - Ranked 2nd:** QIN đạt được vị trí thứ 2 trong EReL@MIR Workshop competition tại WWW 2025. Đây là bằng chứng rằng phương pháp hoạt động tốt trên dữ liệu benchmark tiêu chuẩn được sử dụng trong cuộc thi.

**Model Availability - Code, logs, checkpoints:** Tác giả công bố mã nguồn, training logs, hyperparameters, và model checkpoints trên GitHub, cho phép cộng đồng nghiên cứu reproduce kết quả và xây dựng dựa trên công việc này.

**Inference suitability:** Mặc dù abstract không cung cấp con số latency cụ thể, việc sparse attention design cho thấy QIN được thiết kế để có thể tối ưu hóa cho production deployment, khác với các mô hình multimodal nặng hơn.

## 4. Hạn chế

**Thiếu phân tích chi tiết về latency:** Mặc dù paper được lên kế hoạch để có thể deployment, abstract không cung cấp các số liệu latency suy luận cụ thể hoặc so sánh với các baselines trong aspect này. Để đánh giá đầy đủ về suitability cho production, cần có thông tin về thời gian suy luận.

**Không rõ generalization qua dataset:** Kết quả được báo cáo từ EReL@MIR challenge dataset. Không rõ QIN hoạt động tốt như thế nào trên các dataset multimodal CTR khác (Criteo dataset, Movielens, Yelp, v.v.). Có thể hyperparameters, attention patterns cần tuning riêng cho mỗi domain.

**Thiếu ablation studies:** Abstract không thảo luận về contribution riêng lẻ của adaptive sparse target attention vs. quadratic neural networks. Cái nào quan trọng hơn? Liệu bạn có thể bỏ một trong hai mà vẫn duy trì hiệu suất cao?

**Mức độ sparsity của attention:** Paper không giải thích cách chọn mức độ sparsity (bao nhiêu % phần tử được chọn cho attention). Liệu sparsity là fixed hay adaptive? Sensitivity analysis đối với parameter này sẽ giúp hiểu rõ design choices.

**High competition dataset bias:** EReL@MIR challenge có dataset nhất định và evaluation metrics nhất định. Có khả năng QIN được tuned tốt cho dataset này, nhưng hiệu suất có thể giảm đáng kể khi áp dụng cho các dataset multimodal khác có distribution khác.

**Giới hạn về high-order interactions:** Mặc dù sử dụng quadratic networks, paper không thảo luận về mô hình hóa interactions bậc 3 hoặc cao hơn, hoặc tại sao bậc 2 được chọn là đủ.
