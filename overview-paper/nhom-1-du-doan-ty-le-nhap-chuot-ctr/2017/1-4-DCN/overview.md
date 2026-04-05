# Review Paper: Deep & Cross Network for Ad Click Predictions

**ArXiv ID:** [1708.05123](https://arxiv.org/abs/1708.05123)
**Năm:** 2017
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)
**Tác giả:** Ruoxi Wang, Bin Fu, Gang Fu, Mingliang Wang (Google)

---

## 1. Paper này đang nghiên cứu gì?

Bài paper Deep & Cross Network (DCN) từ Google giải quyết một vấn đề cơ bản trong học sâu cho dự đoán quảng cáo: **các mạng neural sâu học các tương tác đặc trưng một cách ngầm (implicitly) và không nhất thiết hiệu quả** cho các loại tương tác đặc trưng cụ thể cần thiết cho dự đoán CTR.

Bối cảnh nghiên cứu: Mặc dù DNN có khả năng mô hình hóa các tương tác phức tạp, nhưng chúng tạo ra "tất cả" các tương tác mà không có cơ chế nào để chỉ ra hay kiểm soát **mức độ tương tác nào là quan trọng nhất**. Ví dụ, tương tác giữa hai đặc trưng (feature crossing) có thể rất quan trọng, nhưng DNN không có cách hiệu quả để ưu tiên và học những tương tác này so với những đặc trưng đơn lẻ.

**Động lực chính:** Các mô hình trước đó (như Wide & Deep) sử dụng wide component để xử lý tương tác bậc thấp một cách rõ ràng, nhưng đó là thủ công. DCN đặt câu hỏi: **làm thế nào có thể tự động hóa việc tạo và học các crossing tính năng một cách hiệu quả mà không mất quá nhiều overhead tính toán**? Câu trả lời là Cross Network - một cơ chế hoàn toàn mới cho phép học các bounded-degree feature crossing một cách tường minh và hiệu quả.

## 2. Phương pháp sử dụng

DCN giới thiệu **kiến trúc song song với hai thành phần chính: Deep Network và Cross Network**, cùng với một lớp combination layer đơn giản:

**Cross Network (thành phần độc đáo):** Đây là phát minh chính của bài. Một Cross Network gồm nhiều lớp cross (cross layers), trong đó lớp thứ l được định nghĩa như sau:
```
x_{l+1} = x_0 ⊙ (w_l^T x_l + b_l) + x_l
```

Trong đó: x_0 là input ban đầu, x_l là output của lớp l, ⊙ là phép nhân element-wise (Hadamard), w_l và b_l là các tham số học được. Công thức này tạo ra **explicit feature crossing** - mỗi lớp tính toán tích vô hướng giữa input x_l hiện tại với vector trọng số w_l, sau đó nhân từng phần tử với x_0 (input gốc), và cộng lại với x_l để tạo skip connection. Hiệu quả, lớp l này tạo ra tất cả các tương tác bậc l+1 từ input ban đầu.

**Lợi ích của cơ chế này:** (1) Độ phức tạp tính toán chỉ là O(n) với n là số đặc trưng, không phải O(n²). (2) Số tham số cực kỳ nhỏ - chỉ cần một vector trọng số w_l và bias vô hướng cho mỗi lớp. (3) Tự động và rõ ràng học các tương tác bậc cao mà không cần manual engineering.

**Deep Network:** Là một DNN tiêu chuẩn với nhiều lớp fully connected, hàm kích hoạt ReLU, batch normalization, dropout. Thành phần này học các tương tác phức tạp thông qua các biểu diễn tiềm ẩn có kích thước cao.

**Final Combination:** Đầu ra từ Deep Network và Cross Network được concatenate lại với nhau, rồi đi qua một lớp logistic regression cuối cùng để tạo ra xác suất CTR cuối cùng. Điều này cho phép mô hình kết hợp **explicit crossing** từ Cross Network và **implicit complex learning** từ Deep Network.

## 3. Thành tựu đạt được

DCN được đánh giá trên hai tác vụ chính và so sánh với nhiều baseline:

**Trên Criteo CTR Benchmark:** DCN đạt **AUC = 0.8063** (so với Wide & Deep = 0.8012 và DeepCross = 0.8012), cải thiện ~0.6% - một lợi ích đáng kể cho bộ dữ liệu công khai lớn nhất.

**Trên bộ dữ liệu dense classification (Kaggle Display Ads):** DCN đạt **AUCROC = 0.8285** (so với các mô hình cạnh tranh khác), cho thấy mô hình không chỉ tốt cho sparse CTR data mà còn cả dense classification.

**Hiệu suất bộ nhớ:** Cross Network sử dụng **rất ít tham số** - mỗi lớp chỉ cần O(k) tham số (với k là chiều embedding), trong khi DNN cần O(k²) hoặc hơn. Với 6-7 lớp cross và deep network tương tự, DCN vẫn nhẹ hơn cần baseline.

**Tốc độ hội tụ:** DCN hội tụ nhanh hơn Wide & Deep vì Cross Network cung cấp signal rõ ràng về tương tác từ đầu quá trình huấn luyện, thay vì phải chờ DNN tìm hiểu chúng.

**Thử nghiệm trên sản xuất Google Ads:** Mô hình được triển khai vào sản xuất với kết quả: cải thiện online metrics đáng kể trên các truy vấn quảng cáo thực tế, với latency inference thấp hơn Wide & Deep nhờ số lượng tham số ít hơn.

## 4. Hạn chế

**Giới hạn lý thuyết:** (1) Cross Network chỉ tạo ra các tương tác đa thức - cụ thể là tích các đặc trưng được nhân với nhau lặp lại. Nó không thể học các tương tác phi tuyến phức tạp như các hàm phi tuyến của các tương tác này.

(2) Cơ chế explicit crossing tạo ra tất cả các tương tác lên đến bậc l+1 tại lớp l, nhưng không có cách để **chọn lọc** hay **ưu tiên** tương tác nào quan trọng nhất - tất cả đều được tạo.

(3) Cross Network không học được các tương tác thứ tự cao hơn 2 một cách hiệu quả; để có bậc cao hơn cần thêm nhiều lớp, tăng độ phức tạp.

**Thách thức thực tiễn:** (1) Cần điều chỉnh cẩn thận số lượng lớp cross - quá ít thì không đủ crossing, quá nhiều thì overfitting hoặc tăng độ trễ inference.

(2) Công thức cross layer sử dụng x_0 (input ban đầu) - với dữ liệu có kích thước rất lớn (hàng triệu đặc trưng sparse), lưu trữ và sử dụng x_0 trong mỗi lớp có thể tốn bộ nhớ.

(3) Kết hợp đơn giản (concatenation) giữa Deep và Cross output không cho phép tương tác động giữa hai thành phần - chúng vẫn độc lập.

**Hướng tương lai:** (1) Nghiên cứu các cơ chế crossing tinh tế hơn, có khả năng học trọng số hay ưu tiên tương tác.

(2) Kết hợp Cross Network với attention mechanisms để chọn động tương tác quan trọng nhất.

(3) Mở rộng khái niệm crossing đến các tương tác phi tuyến hoặc bậc cao hơn hai.

(4) Áp dụng DCN cho các bài toán prediction khác ngoài quảng cáo như recommendation systems hay fraud detection.
