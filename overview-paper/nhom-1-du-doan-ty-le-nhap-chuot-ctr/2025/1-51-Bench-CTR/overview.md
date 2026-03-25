# Review Paper: Toward a Benchmark for CTR Prediction in Online Advertising: Datasets, Evaluation Protocols and Perspectives

**ArXiv ID:** [2512.01179](https://arxiv.org/abs/2512.01179)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo xác định vấn đề cơ bản trong lĩnh vực dự đoán CTR: thiếu một nền tảng benchmark thống nhất và chuẩn hóa. Hiện tại, các nghiên cứu về dự đoán CTR sử dụng các tập dữ liệu khác nhau, các giao thức đánh giá khác nhau, và các bộ chỉ số khác nhau, làm cho việc so sánh công bằng giữa các phương pháp trở nên khó khăn. Khoảng trống này cản trở sự tiến bộ của lĩnh vực vì không có một "sân chơi" chuẩn hóa để so sánh công bằng các phương pháp mới.

Động lực chính là cần có một nền tảng benchmark tập trung mở rộng, cung cấp các giao thức đánh giá chuẩn hóa, cho phép so sánh công bằng các phương pháp từ các cách tiếp cận thống kê truyền thống cho đến các phương pháp dựa trên LLM hiện đại. Bài báo cũng nhằm cung cấp những hiểu biết chiến lược về hiệu suất tương đối của các phương pháp khác nhau và định hướng cho các nghiên cứu tương lai.

## 2. Phương pháp sử dụng

Bài báo trình bày Bench-CTR, một nền tảng benchmark thống nhất cho dự đoán CTR với các thành phần chính sau:

1. **Giao diện linh hoạt cho các tập dữ liệu:** Cung cấp truy cập chuẩn hóa vào các tập dữ liệu công khai (real-world datasets) và các tập dữ liệu tổng hợp (synthetic datasets). Bài báo sử dụng ba tập dữ liệu công khai và hai tập dữ liệu tổng hợp, cho phép kiểm chứng trên cả dữ liệu thực tế và các tình huống được kiểm soát.

2. **Giao thức đánh giá chuẩn hóa:** Xác định một bộ chỉ số toàn diện (comprehensive metrics) và các hướng dẫn thực nghiệm (experimental guidelines) để đảm bảo so sánh công bằng giữa các phương pháp.

3. **Đánh giá so sánh rộng rãi:** Benchmark tự thực hiện đánh giá trên một loạt rộng các phương pháp, từ các cách tiếp cận thống kê đa biến truyền thống (traditional multivariate statistical methods) cho đến các phương pháp dựa trên LLM hiện đại (LLM-based approaches).

Kỹ thuật cốt lõi của Bench-CTR là cung cấp giao diện thống nhất (unified interface) giúp các nhà nghiên cứu dễ dàng tích hợp các mô hình mới và so sánh hiệu suất của chúng dựa trên một tiêu chuẩn chung.

## 3. Thành tựu đạt được

Bench-CTR cung cấp nhiều hiểu biết chiến lược quan trọng dựa trên đánh giá so sánh rộng rãi:

- **Hiệu suất của mô hình cao cấp:** Các mô hình higher-order hiện đại phát triển tốt hơn đáng kể so với các cách tiếp cận đơn giản (simpler approaches), mặc dù mức độ lợi thế thay đổi tùy thuộc vào chỉ số cụ thể và tập dữ liệu.

- **Hiệu quả dữ liệu của LLM-based models:** Một phát hiện nổi bật là "LLM-based models demonstrate a remarkable data efficiency, i.e., achieving the comparable performance to other models while using only **2% of the training data**". Điều này gợi ý rằng các phương pháp dựa trên LLM có khả năng khái quát hóa vượt trội từ ít dữ liệu hơn.

- **Xu hướng tiến bộ:** Phân tích cho thấy sự cải thiện đáng kể đã xảy ra giữa năm 2015-2016, sau đó tiến bộ đã đình trệ trên các tập dữ liệu hiện tại, gợi ý rằng các phương pháp truyền thống đã đạt tới giới hạn của chúng.

## 4. Hạn chế

Một hạn chế chính là Bench-CTR là một nền tảng đánh giá tĩnh, dựa trên các tập dữ liệu công khai và tổng hợp. Không rõ liệu các kết luận từ các tập dữ liệu này có khái quát hóa tốt sang các bối cảnh sản xuất thực tế khác (ví dụ: các nền tảng quảng cáo khác nhau, các lĩnh vực khác nhau). Dữ liệu công khai thường khác biệt đáng kể so với dữ liệu sản xuất thực tế về sự phân bố đặc trưng và mất cân bằng lớp.

Thứ hai, bài báo chưa cung cấp một cơ chế để đánh giá trên dữ liệu mới khi các mô hình tiếp tục phát triển. Một benchmark tĩnh có thể nhanh chóng trở nên lỗi thời nếu các phương pháp mới vượt qua ngưỡng hiệu suất hiện tại một cách nhanh chóng. Cần có một cơ chế cập nhật định kỳ hoặc xây dựng tập dữ liệu mới.

Thứ ba, bài báo chưa thảo luận chi tiết về chi phí tính toán của các phương pháp khác nhau. Khi so sánh các mô hình, điều quan trọng là phải xem xét không chỉ độ chính xác mà còn hiệu quả tính toán, độ trễ suy luận, và yêu cầu bộ nhớ. Một LLM-based model có thể đạt được hiệu suất tương đương với ít dữ liệu hơn, nhưng nếu nó yêu cầu chi phí tính toán lớn hơn nhiều, điều đó sẽ ảnh hưởng đến tính khả thi sản xuất.
