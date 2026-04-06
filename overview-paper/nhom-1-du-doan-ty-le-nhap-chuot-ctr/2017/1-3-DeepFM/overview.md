# Review Paper: DeepFM - A Factorization-Machine based Neural Network for CTR Prediction

**ArXiv ID:** [1703.04247](https://arxiv.org/abs/1703.04247)
**Năm:** 2017
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)
**Tác giả:** Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, Xiuqiang He

---

## 1. Paper này đang nghiên cứu gì?

Bài paper DeepFM giải quyết vấn đề quan trọng trong dự đoán tỷ lệ nhấp chuột (CTR) cho các hệ thống khuyến nghị: **làm thế nào để học hiệu quả cả tương tác đặc trưng bậc thấp và bậc cao**. Ở thời điểm 2017, mô hình Wide & Deep của Google là phương pháp tiên tiến nhưng có một hạn chế lớn - nó yêu cầu kỹ sư phải thiết kế thủ công các đặc trưng (feature engineering) cho thành phần Wide để nắm bắt các tương tác bậc thấp.

Bài viết nhận thấy rằng dữ liệu quảng cáo điều hành thường chứa hàng triệu đặc trưng thưa thớt (sparse features) - đặc biệt là các biến phân loại được chuyển đổi thành các biểu diễn one-hot. Những tương tác giữa các đặc trưng này (ví dụ: mối quan hệ giữa người dùng, quốc gia, thiết bị, loại quảng cáo) là rất quan trọng nhưng phức tạp để học được.

**Bối cảnh động lực:** Kỹ sư phải thủ công tìm ra những tương tác ngữ nghĩa quan trọng (ví dụ: (người dùng, quốc gia)) và thêm chúng vào dữ liệu đầu vào, việc này tốn thời gian, dễ bỏ sót và không có khả năng tổng quát. DeepFM đề xuất một giải pháp tinh tế: kết hợp Factorization Machines (xử lý tương tác bậc thấp một cách hiệu quả) với Deep Neural Networks (học các tương tác phức tạp bậc cao) trong một kiến trúc thống nhất, giảm đáng kể nhu cầu về kỹ sư đặc trưng thủ công.

## 2. Phương pháp sử dụng

DeepFM sử dụng **kiến trúc song song hai nhánh** kết hợp hai thành phần độc lập:

**Thành phần FM (Factorization Machine):** Học các tương tác bậc nhất và bậc hai giữa các đặc trưng. FM sử dụng các vector tiềm ẩn (latent vectors) để mô hình hóa mỗi đặc trưng, cho phép tính toán các tích vô hướng giữa các cặp đặc trưng một cách hiệu quả với độ phức tạp O(n) thay vì O(n²). Phần FM được định nghĩa riêng biệt với các phần tử tuyến tính và phần tương tác bậc hai.

**Thành phần DNN (Deep Neural Network):** Học các tương tác bậc cao phức tạp thông qua các lớp ẩn được kết nối đầy đủ. Đầu vào của DNN là những embedding của các đặc trưng (chuyển đổi các đặc trưng thưa thớt thành vector liên tục). Các lớp ẩn sử dụng hàm kích hoạt ReLU và các kỹ thuật như batch normalization, dropout để cải thiện huấn luyện.

**Tích hợp chính:** Cả hai thành phần chia sẻ **cùng một lớp embedding** - điều này rất quan trọng. Thay vì tạo hai bộ embedding riêng biệt (như Wide & Deep), DeepFM tận dụng lại cùng một tập hợp vector tiềm ẩn. Điều này giảm kích thước mô hình, giảm số lượng tham số cần học, và cải thiện khả năng tổng quát hóa.

**Hàm mục tiêu:** Cả hai nhánh đều dẫn đến xác suất dự đoán, được kết hợp bằng cách cộng từng đầu ra (FM output + DNN output = final prediction). Sử dụng hàm mất log-likelihood để tối ưu hóa và hàm kích hoạt sigmoid cho đầu ra cuối cùng.

## 3. Thành tựu đạt được

DeepFM được đánh giá trên các bộ dữ liệu công khai và dữ liệu thương mại từ Huawei:

**Trên bộ dữ liệu Criteo CTR:** DeepFM đạt **AUC = 0.8019** (so với Wide & Deep 0.8012), cải thiện khoảng 0.09% nhưng quan trọng hơn là DeepFM không cần feature engineering cho thành phần wide.

**Trên bộ dữ liệu MovieLens-1M (dữ liệu mới):** DeepFM đạt **logloss = 0.543** (so với FM = 0.564, Wide & Deep = 0.547), cho thấy cân bằng tốt giữa tốc độ hội tụ và hiệu suất cuối cùng.

**Trên dữ liệu thương mại Huawei:** DeepFM được triển khai vào sản xuất với khoảng 50 triệu người dùng, đạt cải thiện AUC **0.55% tuyệt đối** so với Wide & Deep, tương ứng với cải thiện doanh thu đáng kể.

**Ưu điểm so với Wide & Deep:** (1) Loại bỏ nhu cầu about feature engineering cho Wide component - chỉ cần raw input, (2) Chia sẻ embedding giảm kích thước mô hình ~30-40%, (3) Hội tụ nhanh hơn vì cách kết nối hai thành phần.

## 4. Hạn chế

**Giới hạn kỹ thuật:** (1) DeepFM vẫn chỉ mô hình hóa tương tác bậc hai rõ ràng thông qua FM; các tương tác bậc cao phải được học ngầm thông qua DNN, điều này có thể không hiệu quả cho một số tương tác cụ thể bậc cao.

(2) Số lượng tham số vẫn tăng tuyến tính với kích thước embedding - với hàng triệu đặc trưng, mô hình có thể vẫn rất lớn.

(3) Cách kết hợp đơn giản (cộng hai output) không cho phép tương tác động giữa thành phần FM và DNN - chúng hoạt động độc lập.

**Những công việc tương lai:** (1) Khám phá các cơ chế kết hợp tinh tế hơn giữa tương tác bậc thấp và cao (chứ không chỉ cộng).

(2) Xử lý các tương tác bậc ba hoặc cao hơn một cách rõ ràng thay vì chỉ ngầm.

(3) Giải quyết vấn đề về sparse data và cold-start problem - khi một đặc trưng mới xuất hiện, mô hình chưa có embedding tốt cho nó.

(4) Tối ưu hóa computational efficiency để có thể mở rộng đến các tập dữ liệu còn lớn hơn với tấc độ inference cao hơn.
