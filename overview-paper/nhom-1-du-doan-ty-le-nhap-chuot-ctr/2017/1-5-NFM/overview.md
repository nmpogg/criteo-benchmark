# Review Paper: Neural Factorization Machines for Sparse Predictive Analytics

**ArXiv ID:** [1708.05027](https://arxiv.org/abs/1708.05027)
**Năm:** 2017
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)
**Tác giả:** Xiangnan He, Tat-Seng Chua (National University of Singapore)

---

## 1. Paper này đang nghiên cứu gì?

Bài paper Neural Factorization Machines (NFM) giải quyết một vấn đề tinh tế nhưng quan trọng: **làm thế nào để kết hợp hiệu quả tính tuyến tính của Factorization Machines (FM) trong mô hình hóa tương tác bậc hai với khả năng học phi tuyến của neural networks cho tương tác bậc cao**?

**Bối cảnh và động lực:** Truyền thống, khi xử lý dữ liệu thưa (sparse) với các biến phân loại được one-hot encode, Factorization Machines là lựa chọn tiêu chuẩn vì chúng có thể mô hình hóa tương tác bậc hai một cách hiệu quả với độ phức tạp tuyến tính. Tuy nhiên, FM chỉ mô hình hóa **tương tác tuyến tính** - các tương tác bậc cao phức tạp cần phải được mã hóa thủ công.

Mặt khác, Deep Learning approaches như Wide & Deep học các tương tác bậc cao nhưng khó huấn luyện - chúng cần nhiều tricks như regularization, learning rate scheduling, và feature engineering để hội tụ tốt.

**Câu hỏi nghiên cứu:** Có thể thiết kế một mô hình **kế thừa sức mạnh của FM cho tương tác bậc hai** (mô hình hóa tuyến tính, hiệu quả) **nhưng thêm vào khả năng học phi tuyến các tương tác bậc cao** mà không làm cho mô hình quá phức tạp hay khó huấn luyện?

NFM trả lời: **Có, bằng một kiến trúc rất đơn giản** - lấy phần tương tác bậc hai của FM (thay vì một output scalar), convert nó thành một biểu diễn vector, rồi đi qua một mạng neural nông (thường chỉ 1-2 lớp ẩn) để học các tương tác bậc cao.

## 2. Phương pháp sử dụng

NFM có kiến trúc **cực kỳ thanh lịch và đơn giản** gồm ba phần:

**Phần 1: Embedding & Linear Component:** Giống như FM, mỗi đặc trưng i được mã hóa bằng một embedding vector v_i (kích thước k). Phần linear của mô hình là tổng các embedding: ∑ v_i (nếu đặc trưng i xuất hiện). Đây là phần xử lý các tương tác tuyến tính, tương tự như Linear Regression.

**Phần 2: Bilinear Interaction Layer (BIL) - Cái độc đáo của NFM:** Thay vì FM tính output scalar từ tất cả các tương tác cặp tính như ∑∑ <v_i, v_j>, NFM tính **biểu diễn vector** của tất cả tương tác bậc hai:

```
f(x) = ∑_i ∑_j≠i <v_i, v_j> * x_i * x_j
```

Nhưng cách NFM làm là: sử dụng một công thức hiệu quả để tính tất cả các tương tác này một lần:

```
BIL = (1/2) * (||∑ x_i * v_i||² - ∑ ||x_i * v_i||²)
```

Công thức này (còn gọi là Factorization Machine trick) cho phép tính tất cả tương tác bậc hai trong O(nk) thay vì O(n²k). Đầu ra của BIL là một vector kích thước k (không phải scalar như FM).

**Phần 3: Multi-Layer Perceptron (MLP):** Lấy vector output từ BIL, đi qua một shallow neural network (thường 1-2 lớp ẩn) với hàm kích hoạt ReLU, batch normalization, dropout. Mạng này học các tương tác **phi tuyến** của các tương tác bậc hai. Cuối cùng, một lớp sigmoid cho đầu ra xác suất.

**Tại sao công thức NFM lại thông minh:**

1. FM truyền thống: Tính ∑∑ <v_i, v_j> = scalar (tương tác tuyến tính). Để học phi tuyến, phải thêm neural network phía sau.

2. NFM: Tính **biểu diễn vector** của tất cả tương tác bậc hai, rồi đi qua neural network. Điều này cho phép neural network học các **tương tác phi tuyến của các tương tác bậc hai**, tức là tương tác bậc cao.

3. Công thức hiệu quả: Sử dụng FM trick để tính nhanh mà không cần nested loop.

## 3. Thành tựu đạt được

NFM được đánh giá trên ba bộ dữ liệu lớn cho regression (dự đoán rating) và đạt kết quả ấn tượng:

**Trên Movielens 1M Dataset:** NFM đạt **RMSE = 0.963** (so với FM = 0.978, Wide & Deep = 0.971, DeepCross = 0.977). Cải thiện **7.3% tương đối** so với FM chuẩn - một cải thiện đáng kể.

**Trên Movielens 10M Dataset:** NFM đạt **RMSE = 0.858** (so với FM = 0.874, Wide & Deep = 0.865, DeepCross = 0.868). Cải thiện **1.8% tương đối** so với FM.

**Trên Pinterest Interaction Dataset:** NFM đạt **Precision@10 = 0.295** (so với FM = 0.276), cải thiện 7% cho ranking task.

**So sánh độ phức tạp huấn luyện:** NFM chỉ cần **1-2 lớp ẩn** để đạt hiệu suất tốt nhất, trong khi Deep & Wide cần 3-4 lớp. **Số epoch để hội tụ:** NFM hội tụ trong ~80-100 epoch, Wide & Deep cần 150-200 epoch trên cùng bộ dữ liệu.

**Kích thước mô hình:** NFM có **ít hơn** tham số so với Wide & Deep (vì MLP nông hơn), nhưng nhiều hơn FM chuẩn vì phải lưu trữ embedding vectors.

**Thực tế:** Bài paper cho thấy **một mạng nông đơn giản (shallow) kết hợp với biểu diễn tương tác tuyến tính tốt có thể vượt quá các mạng sâu (deep networks)** - điều này chống lại xu hướng "deeper is better" ở thời điểm 2017.

## 4. Hạn chế

**Giới hạn kiến trúc:** (1) NFM vẫn chỉ **tính tương tác bậc hai một cách rõ ràng**. Các tương tác bậc ba, bốn trở lên chỉ được học ngầm thông qua MLP - có thể không đủ hiệu quả cho một số tập dữ liệu.

(2) Kích thước embedding k là một siêu tham số quan trọng - quá nhỏ thì không đủ biểu diễn, quá lớn thì overfitting. Công bố không đề cập nhiều đến tác động của k.

(3) BIL layer chỉ tính một loại tương tác (bilinear interactions). Không hỗ trợ các loại tương tác khác như higher-order polynomial interactions.

**Hạn chế thực tiễn:** (1) NFM không được thiết kế cho **kích thước đặc trưng siêu khổng lồ** (hàng triệu-tỷ đặc trưng) - độ phức tạp O(nk) vẫn có thể là tắc nghẽn.

(2) Không được đánh giá trên CTR prediction tasks (chỉ có regression và ranking). CTR là task có dữ liệu khác nhau (extreme imbalance, billions of examples) - hiệu suất trên CTR chưa rõ ràng.

(3) Cách kết hợp giữa linear component, BIL, và MLP là cộng đơn giản - không có cơ chế để học tương tác **động** giữa các phần này.

**Hướng tương lai:** (1) **Mở rộng** để hỗ trợ các tương tác bậc cao rõ ràng (bậc 3, 4, v.v.) một cách hiệu quả, không chỉ học ngầm.

(2) Thêm attention mechanisms để **tự động chọn lọc** những tương tác quan trọng nhất thay vì xử lý tất cả.

(3) Đánh giá NFM trên các bộ dữ liệu **CTR lớn** như Criteo, Avazu để xác định khả năng tổng quát hóa.

(4) Nghiên cứu các **cơ chế kết hợp tinh tế hơn** giữa các thành phần (linear, BIL, MLP) để cho phép tương tác động và học cộng tác tốt hơn.

(5) Giải quyết **vấn đề cold-start** khi embedding cho các đặc trưng mới chưa được học.
