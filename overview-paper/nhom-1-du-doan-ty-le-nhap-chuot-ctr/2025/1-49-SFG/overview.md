# Review Paper: From Feature Interaction to Feature Generation: A Generative Paradigm of CTR Prediction Models

**ArXiv ID:** [2512.14041](https://arxiv.org/abs/2512.14041)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo xác định hai hạn chế cơ bản trong các mô hình phân biệt truyền thống để dự đoán CTR. Thứ nhất là "embedding dimensional collapse" — hiện tượng mà các embedding không sử dụng đầy đủ không gian biểu diễn có sẵn. Thứ hai là "information redundancy" — thông tin dư thừa trong các embedding dẫn đến một phần không cần thiết. Hai vấn đề này phát sinh từ việc phụ thuộc quá mức vào mô hình hóa tương tác đặc trưng và bỏ qua các embedding ID thô.

Khoảng trống trong nghiên cứu hiện tại là không có một paradigm cơ bản nào thực sự giải quyết vấn đề collapse và redundancy thông qua một cách tiếp cận khác. Hầu hết các phương pháp hiện tại chỉ tập trung vào việc mô hình hóa tương tác tốt hơn, mà không giải quyết các vấn đề cơ bản về biểu diễn embedding. Động lực chính là cần một sự thay đổi paradigm từ tương tác đặc trưng sang sinh tạo đặc trưng để cải thiện chất lượng embedding.

## 2. Phương pháp sử dụng

Bài báo đề xuất framework Supervised Feature Generation (SFG) chuyển đổi paradigm từ "feature interaction" phân biệt sang "feature generation" sinh tạo. Kiến trúc SFG gồm hai thành phần chính:

1. **Encoder:** Xây dựng các hidden embeddings từ raw feature embeddings thông qua các phép biến đổi học được, nén thông tin từ các embedding gốc thành các biểu diễn tiềm ẩn.

2. **Decoder:** Tái tạo lại các feature embeddings từ hidden representations, buộc mô hình học các biểu diễn compressed có ý nghĩa mà giữ lại thông tin thiết yếu.

Điểm khác biệt chính so với các cách tiếp cận sinh tạo trước đây là SFG sử dụng "supervised loss" thay vì "self-supervised loss". Điều này có nghĩa là loss function tận dụng tín hiệu giám sát trực tiếp (click hoặc không click) từ nhiệm vụ dự đoán CTR, không phải chỉ tái tạo đầu vào. Framework này tích hợp liền mạch với các mô hình CTR hiện tại dưới paradigm sinh tạo, cho phép sử dụng linh hoạt với nhiều kiến trúc cơ sở khác nhau.

## 3. Thành tựu đạt được

SFG đạt được các cải thiện hiệu suất đáng kể trên nhiều tập dữ liệu công khai và với các mô hình cơ sở khác nhau. Bài báo báo cáo "substantial performance gains" được xác nhận trên các dataset đa dạng và nhiều baselines khác nhau, giảm embedding collapse và giảm redundancy thông tin một cách đáng kể.

Sự cải thiện được đo lường thông qua các độ đo chuẩn trong dự đoán CTR (AUC, LogLoss), cho thấy tính hiệu quả của paradigm sinh tạo. Framework được kiểm chứng trên các mô hình cơ sở khác nhau, chứng tỏ khả năng tổng quát hóa và tính linh hoạt. Bài báo cũng cung cấp code trên GitHub, cho phép các nhà nghiên cứu khác kiểm chứng kết quả và xây dựng trên công trình này.

## 4. Hạn chế

Một hạn chế chính là chi phí tính toán bổ sung từ encoder-decoder architecture. Bài báo không cung cấp phân tích chi tiết về độ phức tạp thời gian và không gian, hoặc tác động lên độ trễ suy luận trong môi trường sản xuất. Việc thêm một decoder layer có thể tăng độ trễ thời gian thực, điều này quan trọng trong các hệ thống quảng cáo có độ trễ thấp.

Thứ hai, bài báo chưa cung cấp bằng chứng thực nghiệm sản xuất (online A/B testing) từ nền tảng quảng cáo công nghiệp lớn. Mặc dù kết quả offline rất tốt, việc thiếu xác minh sản xuất làm giảm khả năng tin tưởng của tác động thực tế trong các hệ thống sản xuất quy mô lớn.

Thứ ba, bài báo chưa thảo luận đầy đủ về các giả định dưới đó phương pháp hoạt động tốt. Ví dụ, liệu supervised loss có hoạt động tốt với các loại dữ liệu mất cân bằng nặng nề (class imbalance) không? Làm thế nào phương pháp mở rộng với các embedding động hoặc thay đổi theo thời gian? Những câu hỏi này còn chưa được giải quyết.
