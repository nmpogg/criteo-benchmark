# Review Paper: Learning to Embed Categorical Features without Embedding Tables for Recommendation

**ArXiv ID:** [2010.10784](https://arxiv.org/abs/2010.10784)
**Năm:** 2020
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding của các đặc trưng phân loại (categorical features) như user ID hoặc item ID là yếu tố cốt lõi trong các mô hình gợi ý hiện đại, từ matrix factorization đến neural collaborative filtering. Phương pháp tiêu chuẩn hiện tại là tạo một bảng embedding nơi mỗi hàng đại diện cho một vector embedding riêng biệt cho mỗi giá trị đặc trưng duy nhất.

Tuy nhiên, phương pháp này gặp hai thách thức lớn: Thứ nhất, nó không xử lý hiệu quả các đặc trưng có cardinality cao (ví dụ như video ID trong YouTube với hàng triệu video). Thứ hai, nó không thể xử lý các giá trị đặc trưng chưa thấy (unseen feature values) như video mới vừa được upload, vì những giá trị này không có embedding vector được huấn luyện trước đó.

## 2. Phương pháp sử dụng

Bài báo đề xuất Deep Hash Embedding (DHE), một framework thay thế bảng embedding truyền thống bằng một mạng neural sâu để tính toán embedding động khi chạy (on-the-fly). Phương pháp này bao gồm hai thành phần chính:

**Thành phần Encoding:** Sử dụng các hàm hash và phép biến đổi để tạo các vector định danh duy nhất từ các feature value. Đây là một thành phần xác định (deterministic), không khả học (non-learnable), và không cần lưu trữ. Các hàm hash được áp dụng để chuyển đổi feature value thô thành một biểu diễn mã hóa.

**Thành phần Mạng Neural:** Một DNN khả học chuyển đổi các vector định danh đã mã hóa thành embedding vectors. Thành phần này là learnable và được huấn luyện end-to-end. Kiến trúc này cho phép DHE xử lý cả các giá trị đặc trưng đã thấy lẫn chưa thấy bằng cách tính toán embedding tức thời từ mã hóa của chúng.

## 3. Thành tựu đạt được

Deep Hash Embedding đạt được AUC so sánh được với phương pháp embedding table tiêu chuẩn (one-hot full embedding) nhưng với kích thước mô hình nhỏ hơn đáng kể. Phương pháp giảm bộ nhớ lưu trữ cho embedding layer từ O(n*d) với phương pháp truyền thống (n là số giá trị feature unique, d là chiều embedding) xuống một lượng đáng kể nhỏ hơn.

Framework đặc biệt hiệu quả đối với các đặc trưng có cardinality cao và xử lý rất tốt các giá trị feature chưa thấy. Kết quả thí nghiệm được trình bày trên các bộ dữ liệu recommendation thực tế, chứng minh rằng DHE có thể tương tranh với các phương pháp baseline trong khi sử dụng ít bộ nhớ hơn đáng kể.

## 4. Hạn chế

Một hạn chế đáng chú ý là overhead tính toán của DNN trong quá trình inference so với việc tra cứu bảng embedding đơn giản. Mỗi lần cần embedding cho một feature value mới, phải chạy qua toàn bộ DNN encoder thay vì chỉ tra cứu bảng O(1), điều này có thể gây chậm trễ trong hệ thống production.

Thứ hai, hiệu quả của phương pháp phụ thuộc vào chất lượng của các hàm hash và chiều của vector mã hóa. Nếu các hàm hash không phân biệt được tốt giữa các feature value khác nhau, DNN sẽ phải học được từ các biểu diễn mã hóa trùng lặp, có thể dẫn đến loss chất lượng embedding. Ngoài ra, paper không cung cấp chi tiết về scalability của phương pháp khi số lượng giá trị feature tăng lên rất lớn.
