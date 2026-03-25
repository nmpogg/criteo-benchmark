# Review Paper: HE-LRM - Encrypted Embedding via FHE

**ArXiv ID:** [2506.18150](https://arxiv.org/abs/2506.18150)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

HE-LRM nhắm tới vấn đề bảo mật trong neural inference, cụ thể là thực hiện các tính toán model mà không tiết lộ dữ liệu đầu vào hoặc trọng số mô hình cho bên thứ ba. Khi sử dụng dịch vụ inference trên cloud, đó là mối lo ngại bảo mật lớn. Bài báo tập trung vào Deep Learning Recommendation Models (DLRM) - một kiến trúc quan trọng trong công nghiệp, nơi embedding lookups chiếm một phần đáng kể của tính toán.

Vấn đề kỹ thuật chính là fully homomorphic encryption (FHE) rất chậm, đặc biệt khi thực hiện các phép tìm kiếm embedding (embedding lookups). Trong FHE, mỗi phép toán nhân đơn giản yêu cầu một "multiplicative level", và khi hết tất cả level, phải thực hiện bootstrap (mất ~20 giây). Các phương pháp trước sử dụng one-hot encoding dẫn đến lãng phí slot và tiêu tốn nhiều level nhân.

HE-LRM giải quyết thách thức này bằng cách phát triển các kỹ thuật tối ưu hóa hiệu suất cho embedding lookups dưới FHE, cho phép inference end-to-end trên dữ liệu được mã hóa với latency có thể chấp nhận được.

## 2. Phương pháp sử dụng

HE-LRM giới thiệu ba đóng góp kỹ thuật chính:

**Thứ nhất, Digit Decomposition Compression**: Thay vì sử dụng one-hot encoding (k-element vector chỉ có một phần tử 1), HE-LRM phân tách (decompose) các embedding indices thành base-p digits. Cụ thể, một bảng embedding có k hàng được biểu diễn dưới dạng ℓ bảng nhỏ hơn, mỗi bảng có p hàng, với k=p^ℓ. Phương pháp này được thực hiện client-side, giải phóng cho server khỏi cần tính toán các indicator function phức tạp dưới mã hóa. Kỹ thuật này chỉ tiêu tốn một multiplicative level duy nhất (so với CodedHeLUT cần 2+r+2s levels), đạt speedup 56× so với state-of-the-art trước đó.

**Thứ hai, Multi-Embedding Block-Diagonal Packing**: Để xử lý các DLRM có nhiều bảng embedding, HE-LRM sắp xếp các bảng embedding theo cấu trúc block-diagonal trong một ma trận trọng số. Client side tạo one-hot vectors cho mỗi bảng, nối chúng lại với nhau, rồi mã hóa thành một ciphertext duy nhất. Cách tiếp cận này cho phép các embedding lookup song song (parallel) trên nhiều bảng đồng thời, tối đa hóa sử dụng slot trong CKKS scheme và duy trì compatibility với các phép toán downstream.

**Thứ ba, CKKS Encryption Framework**: Hệ thống được xây dựng trên CKKS (Cheon-Kim-Kim-Song) scheme, cho phép encrypted SIMD operations. Mỗi ciphertext chứa ~2^15 slots, hỗ trợ các phép toán như cộng phần tử, nhân phần tử, và rotation tuần hoàn. Output embeddings được đặt trong các slot liên tiếp để có thể truyền trực tiếp tới các layer tiếp theo.

## 3. Thành tựu đạt được

HE-LRM đạt được các kết quả hiệu suất đáng chú ý:

**UCI Heart Disease Dataset**: Latency end-to-end là 24 giây trên CPU single-threaded, duy trì 85% validation accuracy với x² activation function. Đây là một cải thiện đáng kể so với các phương pháp trước.

**Criteo Dataset (Industry-scale)**: Hệ thống đạt latency 489 giây cho các mô hình dựa trên ReLU trên bộ dữ liệu Criteo quy mô công nghiệp. Tuy nhiên, tỉ lệ nén đạt được là 31,180×, cho thấy khả năng nén dữ liệu mạnh mẽ của phương pháp.

**Projection hiệu suất**: Dự báo hiệu suất trên GPU là ~1 giây, và trên ASIC chuyên dụng là ~37 milliseconds. Các con số này gợi ý rằng với tối ưu hóa phần cứng, phương pháp có thể đạt tới latency thực tiễn.

**Speedup đặc biệt**: Digit decomposition đạt 56× speedup so với prior art, một cải thiện vượt trội cho phép FHE-based inference trở nên khả thi hơn trong thực tế.

## 4. Hạn chế

HE-LRM có một số hạn chế cần lưu ý. Thứ nhất, latency tuyệt đối trên CPU vẫn còn cao (24-489 giây), khiến giải pháp chỉ khả thi cho các ứng dụng không cần thời gian phản hồi tức thì. Thứ hai, phương pháp chỉ được đánh giá trên hai dataset (UCI và Criteo) với kích thước embedding bảng khác nhau, không rõ khả năng tổng quát trên các bộ dữ liệu khác.

Thứ ba, công việc tập trung vào embedding lookups nhưng không khám phá tối ưu hóa FHE cho các phần khác của mô hình (dense layers, activations). Thứ tư, overhead key management và ciphertext communication trong môi trường thực tế không được phân tích chi tiết.

Công việc tương lai cần tối ưu hóa phần cứng để giảm latency tuyệt đối, mở rộng sang các kiến trúc model khác, và xây dựng các lược đồ hybrid kết hợp FHE với các kỹ thuật bảo mật khác để cân bằng bảo mật và hiệu suất.
