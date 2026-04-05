# Review Paper: Tensorized Embedding Layers for Efficient Model Compression

**ArXiv ID:** [1901.10787](https://arxiv.org/abs/1901.10787)
**Năm:** 2019
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo tập trung vào vấn đề nén tầng embedding trong các mô hình deep learning cho xử lý ngôn ngữ tự nhiên (NLP). Động lực của bài báo xuất phát từ thực tế là khi từ vựng rất lớn, ma trận trọng số tầng embedding có thể trở nên khổng lồ, tiêu tốn hàng chục tới hàng trăm GB bộ nhớ, làm cản trở việc triển khai mô hình trên các thiết bị có tài nguyên hạn chế (mobile, edge devices).

Khoảng cách trong nghiên cứu hiện tại là không có cách tiếp cận nào có thể nén embedding một cách đáng kể (significant compression) đồng thời giữ hoặc thậm chí cải thiện hiệu suất mô hình. Hầu hết các phương pháp nén embedding hiện tại gây ra sụt giảm đáng chú ý về độ chính xác. Do đó, nhu cầu về một phương pháp nén embedding hiệu quả mà không ảnh hưởng (hoặc thậm chí cải thiện) đến kết quả là rất cấp thiết, đặc biệt cho các ứng dụng triển khai trên thiết bị giới hạn tài nguyên.

## 2. Phương pháp sử dụng

Bài báo đề xuất sử dụng **Tensor Train (TT) decomposition** để tham số hóa các tầng embedding. Thay vì lưu trữ trực tiếp ma trận embedding kích thước $|V| \times d$ (với $|V|$ là kích thước từ vựng và $d$ là chiều embedding), phương pháp này phân tích ma trận thành một tích của các tensor nhỏ hơn thông qua công thức Tensor Train.

Cơ chế hoạt động: Tensor Train biểu diễn một tensor đa chiều dưới dạng một chuỗi (chain) của các ma trận nhỏ hơn gọi là "cores". Khi áp dụng vào embedding layer, mỗi core có kích thước nhỏ hơn đáng kể so với ma trận gốc. Điều này cho phép giảm số lượng tham số cần lưu trữ và tính toán, trong khi vẫn có khả năng biểu diễn đầy đủ các embedding vectors.

Lợi thế kỹ thuật của TT decomposition là nó cung cấp một sự cân bằng tốt giữa khả năng biểu diễn (expressiveness) và độ nén (compression ratio). Tensor Train là một phương pháp phân tích nhân tử (factorization) đã được chứng minh trong nhiều ứng dụng machine learning, với tính ổn định số học tốt và khả năng hội tụ nhanh trong quá trình huấn luyện.

## 3. Thành tựu đạt được

Bài báo đánh giá phương pháp trên một loạt rộng các benchmark NLP với các kiến trúc khác nhau bao gồm MLPs, LSTMs, và Transformers. Kết quả cho thấy phương pháp TT decomposition có thể **nén mô hình một cách đáng kể với sụt giảm hiệu suất không đáng kể hoặc thậm chí cải thiện nhẹ hiệu suất** (negligible drop or slight gain in performance).

Các benchmark được sử dụng bao gồm nhiều tác vụ NLP khác nhau từ phân loại văn bản, machine translation, đến question answering trên các mô hình có kích thước từ nhỏ đến lớn. Phương pháp cho thấy khả năng thích ứng cao với các kiến trúc khác nhau, từ mô hình đơn giản (MLPs) đến các mô hình hiện đại (Transformers).

Điểm quan trọng là bài báo cung cấp phân tích chi tiết về mối quan hệ trade-off giữa hiệu suất (performance) và tỉ lệ nén (compression ratio) trên nhiều kiến trúc khác nhau, giúp từ chối tuyên bố chung chung mà cung cấp cái nhìn thực tế về các trường hợp sử dụng cụ thể.

## 4. Hạn chế

Một hạn chế tiềm năng của phương pháp là chi phí tính toán của quá trình phân tích Tensor Train. Mặc dù số lượng tham số giảm, việc tính toán forward pass qua các cores của TT có thể tăng độ phức tạp tính toán, đặc biệt là trong quá trình inference trên các thiết bị với đơn vị tính toán hạn chế.

Bên cạnh đó, Tensor Train decomposition có các siêu tham số (rank, core dimensions) mà cần được điều chỉnh cho từng bài toán cụ thể. Việc lựa chọn các siêu tham số này không phải lúc nào cũng tầm thường, và có thể đòi hỏi một quá trình grid search hoặc cross-validation tốn thời gian. Khả năng tổng quát hóa của phương pháp trên các bài toán NLP khác nhau cũng chưa được kiểm chứng đầy đủ, và hiệu suất có thể phụ thuộc vào đặc điểm cụ thể của từ vựng (distribution của độ tần suất từ, độ dài từ, v.v.) trong từng bài toán.

Cuối cùng, bài báo tập trung chủ yếu vào việc nén tầng embedding và không xem xét cách phương pháp này có thể được mở rộng để nén các tầng khác của mô hình (fully connected layers, convolutional layers, etc.), giới hạn phạm vi áp dụng của đóng góp này.

---

**Unresolved Questions:**
- Chi phí tính toán thực tế của TT decomposition trên inference là bao nhiêu so với embedding trực tiếp?
- Làm thế nào để tự động chọn các siêu tham số (rank, core dimensions) tối ưu mà không cần grid search?
- Phương pháp này có khả năng tổng quát hóa tốt không khi áp dụng trên các tác vụ NLP hoàn toàn mới?
