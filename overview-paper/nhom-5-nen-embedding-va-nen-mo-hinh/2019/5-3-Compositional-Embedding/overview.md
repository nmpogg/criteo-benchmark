# Review Paper: Compositional Embeddings Using Complementary Partitions for Memory-Efficient Recommendation Systems

**ArXiv ID:** [1909.02107](https://arxiv.org/abs/1909.02107)
**Năm:** 2019
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo tập trung vào vấn đề tắc nghẽn bộ nhớ trong các hệ thống deep learning recommendation xử lý hàng trăm ngàn (hoặc hàng triệu) đặc trưng phân loại (categorical features). Động lực là embedding tables là thành phần chính tiêu tốn bộ nhớ khi hệ thống phải lưu trữ embedding vectors cho tất cả các giá trị khác nhau của mỗi categorical feature. Ví dụ, một feature "product_id" có 100 triệu sản phẩm sẽ cần lưu trữ 100 triệu embedding vectors, mỗi vector có kích thước d chiều - điều này dễ dàng yêu cầu hàng chục đến hàng trăm gigabyte bộ nhớ.

Khoảng cách trong nghiên cứu hiện tại là các phương pháp nén embedding hiện có như "hashing trick" (sử dụng hash functions để ánh xạ nhiều giá trị feature thành cùng một embedding vector) gây ra collision - nhiều giá trị khác nhau bị ánh xạ thành một embedding, dẫn đến mất mát thông tin. Cần có một phương pháp cho phép tạo một unique embedding vector cho mỗi danh mục (category) mà không cần định nghĩa tường minh từng embedding, đồng thời giảm đáng kể lượng bộ nhớ sử dụng.

## 2. Phương pháp sử dụng

Bài báo đề xuất phương pháp **Compositional Embeddings sử dụng Complementary Partitions**. Ý tưởng cốt lõi là thay vì lưu trữ một embedding table đơn lẻ với mỗi category có một hàng riêng, phương pháp này sử dụng multiple smaller embedding tables được phát sinh từ các complementary partitions (các phân hoạch bù nhau) của tập hợp các category.

Cơ chế hoạt động cụ thể: Giả sử có N danh mục và cần M embedding tables nhỏ hơn. Phương pháp chia tập hợp N danh mục thành M phân hoạch bù nhau (complementary partitions) - mỗi danh mục xuất hiện trong chính xác k phân hoạch và các phân hoạch không trùng lặp một cách tối ưu. Với cách này, embedding vector của một category c được tạo ra bằng cách **kết hợp (compose)** các embedding vectors từ k embedding tables nhỏ tương ứng với các phân hoạch mà category đó thuộc về.

Điều này giống như sử dụng một "codebook cố định" để đảm bảo mỗi category có một biểu diễn embedding unique. Thay vì lưu trữ N embedding vectors kích thước d, phương pháp này chỉ cần lưu trữ M embedding tables có kích thước N/k × d, tiết kiệm bộ nhớ theo tỷ lệ khoảng M·(1/k) ≈ log(N).

## 3. Thành tựu đạt được

Bài báo đánh giá phương pháp trên các bộ dữ liệu recommendation system quy mô lớn và so sánh với hashing trick - một baseline tiêu chuẩn để nén embedding tables. Kết quả thí nghiệm chứng minh:

- Phương pháp Compositional Embeddings **hiệu quả hơn hashing trick** trong việc giảm kích thước embedding tables
- Đạt được **cải thiện model loss và accuracy** so với hashing trick, cho thấy việc sử dụng complementary partitions tốt hơn random hashing
- Giữ được **comparable parameter reduction** (sụt giảm số lượng tham số tương tự) với hashing trick nhưng với chất lượng tốt hơn

Bài báo bao gồm 11 trang với 7 hình vẽ và 1 bảng dữ liệu, cho thấy sự phân tích chi tiết về các trade-off giữa kích thước embedding table, số lượng embedding tables, và hiệu suất mô hình. Các thí nghiệm trên các datasets thực tế từ công ty recommendation systems lớn chứng minh tính thực tiễn và tính mở rộng của phương pháp.

## 4. Hạn chế

Một hạn chế lớn của phương pháp là chi phí tính toán của việc tổng hợp (composing) embedding vectors từ nhiều embedding tables. Thay vì một phép truy cập bộ nhớ (memory lookup) duy nhất như trong embedding thông thường, phương pháp này cần k phép truy cập bộ nhớ và sau đó thực hiện một phép toán tổng hợp (có thể là concatenation, addition, hoặc một phép toán phức tạp hơn) trên k vectors. Điều này tăng độ phức tạp tính toán trong forward pass, đặc biệt quan trọng trong các hệ thống recommendation có latency constraints cao.

Thứ hai, phương pháp phụ thuộc vào lựa chọn cấu trúc complementary partitions. Tìm kiếm cấu trúc partitions tối ưu có thể là một bài toán NP-hard, và bài báo không rõ ràng nêu cách thức xác định partitions tối ưu cho một bộ dữ liệu cụ thể. Nếu cấu trúc partitions không được chọn tốt, hiệu suất của phương pháp có thể sụt giảm đáng kể.

Cuối cùng, bài báo chỉ so sánh với hashing trick mà không so sánh với các phương pháp nén embedding khác hoặc các kỹ thuật phân tích nhân tử (factorization techniques) khác. Khả năng tổng quát hóa trên các loại categorical features khác nhau (features với phân phối tuân theo power law vs. features với phân phối đều) chưa được đánh giá đầy đủ. Ngoài ra, phương pháp này chỉ tập trung vào embedding layer và không xem xét tích hợp với các kỹ thuật nén mô hình khác.

---

**Unresolved Questions:**
- Làm thế nào để xác định cấu trúc complementary partitions tối ưu một cách hiệu quả mà không cần grid search?
- Chi phí tính toán (latency overhead) của việc tổng hợp embeddings từ k tables là bao nhiêu trên các hardware recommendation khác nhau?
- Phương pháp này có hoạt động tốt không khi phân phối của categorical features thay đổi giữa training và serving?
- Làm thế nào để kết hợp phương pháp này với các kỹ thuật nén khác (weight quantization, pruning) để đạt nén toàn mô hình?
