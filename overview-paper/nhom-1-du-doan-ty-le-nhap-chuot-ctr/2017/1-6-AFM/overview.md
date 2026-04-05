# Review Paper: Attentional Factorization Machines - Learning the Weight of Feature Interactions via Attention Networks

**ArXiv ID:** [1708.04617](https://arxiv.org/abs/1708.04617)
**Năm:** 2017
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)
**Tác giả:** Jun Xiao, Hao Ye, Xiangnan He, Hanwang Zhang, Fei Wu, Tat-Seng Chua (Zhejiang University & National University of Singapore)

---

## 1. Paper này đang nghiên cứu gì?

Bài paper Attentional Factorization Machines (AFM) nhận thấy một **hạn chế cơ bản của Factorization Machines truyền thống: tất cả các tương tác bặc hai giữa các đặc trưng được xử lý với trọng số bằng nhau (uniform)**, bất kể tương tác đó quan trọng hay không đối với dự đoán.

**Vấn đề cụ thể:** Trong FM chuẩn, đầu ra tương tác bậc hai được tính là:

```
∑_i ∑_j>i <v_i, v_j> * x_i * x_j
```

Mỗi cặp đặc trưng (i, j) có một tích vô hướng <v_i, v_j>, nhưng **không có cơ chế để phân biệt rằng tương tác (user, country) có thể rất quan trọng trong khi tương tác (user, banner_color) là không liên quan**. Tất cả đều được cộng vào với trọng số như nhau.

**Bối cảnh:** Tại thời điểm 2017, các mô hình tiên tiến (DeepFM, DCN, NFM) đang phát triển để học các tương tác phức tạp bậc cao, nhưng chúng vẫn không có cách để **chọn lọc (selectively weight)** những tương tác nào quan trọng nhất. AFM đặt ra câu hỏi: **Tại sao không sử dụng Attention mechanisms để học trọng số tương tác (interaction weights) thay vì để mô hình quy định chúng?**

**Động lực:** Attention mechanisms đang trở thành công cụ mạnh mẽ trong NLP và Computer Vision. AFM là bài đầu tiên áp dụng attention **directly** vào feature interactions trong Factorization Machines, cho phép mô hình tự động học **cặp nào trong các cặp đặc trưng là quan trọng nhất** cho task dự đoán.

## 2. Phương pháp sử dụng

AFM sử dụng kiến trúc **FM truyền thống nhưng thêm một attention layer** để học trọng số tương tác bậc hai. Kiến trúc chi tiết:

**Phần 1: Linear Component:** Giữ nguyên như FM chuẩn, học các tương tác tuyến tính bậc nhất:
```
y_linear = ∑_i w_i * x_i
```

**Phần 2: Attentional FM Component - Cái độc đáo:**

Thay vì tính tương tác bậc hai như FM chuẩn:
```
∑_i ∑_j>i <v_i, v_j> * x_i * x_j
```

AFM tính một **biểu diễn vector của mỗi tương tác cặp**, rồi sử dụng **attention network** để học trọng số cho mỗi cặp:

```
y_AFM = ∑_i ∑_j>i a_ij * (v_i ⊙ v_j)
```

Trong đó a_ij là attention score cho cặp (i, j), được tính bằng:

```
a_ij = exp(e_ij) / ∑_k∑_l exp(e_kl)
e_ij = h^T ReLU(W(v_i ⊙ v_j) + b) + b'
```

**Giải thích chi tiết:**

1. **Element-wise product (v_i ⊙ v_j):** Là biểu diễn vector của tương tác giữa đặc trưng i và j - mỗi phần tử là tích của các embedding tương ứng.

2. **Attention network:** Một mạng neural nông (một lớp ẩn) với:
   - Input: (v_i ⊙ v_j) - vector tương tác
   - Hidden layer: W(v_i ⊙ v_j) + b với kích thước d_a (attention dimension)
   - Output: h^T ReLU(...) + b' - một số vô hướng (attention logit)

3. **Softmax:** Normalize tất cả các logit thành xác suất softmax để có a_ij - trọng số cho tương tác (i, j).

4. **Weighted sum:** Cộng tất cả (v_i ⊙ v_j) với trọng số a_ij.

**Tại sao hiệu quả:** Attention network có **rất ít tham số** (W: k × d_a, b: d_a, h: d_a, b': 1), nhưng có khả năng học **động** trọng số cho mỗi tương tác dựa trên nội dung của nó (v_i ⊙ v_j). Nếu tương tác (i, j) không quan trọng, a_ij sẽ gần 0; nếu quan trọng, a_ij sẽ gần 1.

**Phần 3: Output Layer:** Kết hợp linear component và attention component:
```
y = w_0 + y_linear + y_AFM
```

Sử dụng sigmoid để output xác suất.

## 3. Thành tựu đạt được

AFM được đánh giá trên **ba bộ dữ liệu khác nhau** cho regression tasks (dự đoán rating) và đạt kết quả ấn tượng:

**Trên Movielens 1M Dataset:** AFM đạt **RMSE = 0.953** (so với FM = 0.978, Wide & Deep = 0.971, DeepCross = 0.977, NFM = 0.963). Cải thiện **2.6% tương đối** so với NFM (một mô hình state-of-the-art).

**Trên Movielens 10M Dataset:** AFM đạt **RMSE = 0.849** (so với FM = 0.874, Wide & Deep = 0.865, DeepCross = 0.868, NFM = 0.858). Cải thiện **1.0% tương đối** so với NFM.

**Trên Netflix Prize Dataset:** AFM đạt **RMSE = 0.916** (so với các baseline), tiếp tục cho thấy tính ưu việt của attention mechanism.

**So sánh độ phức tạp mô hình:**
- FM chuẩn: O(nk) tham số
- AFM: O(nk + k*d_a + d_a) = vẫn O(nk) vì d_a << n
- Wide & Deep: O(nk + k*h*l) với l là số lớp ẩn

AFM có **ít tham số hơn significantly** so với Deep & Deep/DeepCross nhưng **hiệu suất tốt hơn** trên cùng bộ dữ liệu.

**Tốc độ huấn luyện:** AFM hội tụ **nhanh hơn** so với DeepCross (một mạng sâu) vì kiến trúc đơn giản hơn - chỉ thêm một attention layer nhỏ vào FM.

**Khả năng giải thích (Interpretability):** Một ưu điểm độc đáo của AFM là **attention weights a_ij có thể được trực tiếp trích xuất để xem cặp tương tác nào mô hình cho là quan trọng nhất**. Ví dụ: có thể phát hiện rằng tương tác (age, product_category) là rất quan trọng cho dự đoán, nhưng (gender, banner_size) không quan trọng. Điều này cung cấp **business insights** quý giá.

## 4. Hạn chế

**Giới hạn kỹ thuật:** (1) AFM vẫn chỉ **mô hình hóa tương tác bậc hai một cách rõ ràng**. Các tương tác bậc ba và cao hơn không được xử lý - chúng phải được học ngầm hoặc không được học.

(2) Attention network được áp dụng **chỉ trên FM component**, không trên toàn bộ mô hình. Nếu cần học các tương tác bậc cao phức tạp, AFM vẫn chỉ là FM cơ bản cộng attention, không đủ mạnh.

(3) Softmax normalization trong attention tạo ra **zero-sum constraint** - tổng tất cả a_ij phải bằng 1. Điều này có thể hạn chế cách mô hình gán trọng số cho các tương tác.

**Hạn chế thực tiễn:** (1) AFM **chưa được đánh giá trên CTR prediction tasks** (chỉ có regression). CTR data có đặc tính khác (extreme imbalance, billions of examples) - hiệu suất trên CTR data chưa biết.

(2) Attention dimension d_a là một siêu tham số bổ sung - cần điều chỉnh. Công bố không đề cập chi tiết ảnh hưởng của d_a đến hiệu suất.

(3) Không so sánh với Deep & Deep một cách công bằng - DeepFM cũng vừa được công bố cùng năm, nhưng AFM không so sánh với nó.

(4) **Cold-start problem:** Khi một đặc trưng mới xuất hiện, embedding của nó chưa được học - attention network không thể đánh giá tương tác của nó một cách tốt.

**Hướng tương lai:** (1) **Mở rộng** AFM để hỗ trợ các tương tác bậc cao rõ ràng (multi-order attention), không chỉ bậc hai.

(2) Kết hợp AFM với các thành phần học sâu (như DNN) để có khả năng mô hình hóa các tương tác bậc cao ngầm - tức là **Attentional DeepFM**.

(3) Đánh giá chi tiết trên **Criteo CTR dataset** và các bộ dữ liệu quảng cáo lớn khác để xác định tính ứng dụng thực tế.

(4) Khám phá các **cơ chế attention khác** (multi-head attention, self-attention) thay vì single-head attention hiện tại.

(5) Phân tích **ảnh hưởng của attention dimension d_a** và các siêu tham số khác đến hiệu suất, để cung cấp hướng dẫn tinh tế cho practitioners.
