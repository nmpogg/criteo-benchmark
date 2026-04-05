# Review Paper: FiBiNET - Combining Feature Importance and Bilinear Feature Interaction for CTR Prediction

**ArXiv ID:** [1905.09433](https://arxiv.org/abs/1905.09433)  
**Năm:** 2019  
**Venue:** ACM RecSys 2019  
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)

---

## 1. Paper này đang nghiên cứu gì?

FiBiNET (Feature Importance and Bilinear feature Interaction NETwork) giải quyết một vấn đề quan trọng nhưng thường bị bỏ qua trong dự đoán CTR: **tầm quan trọng không đều của các đặc trưng và cách mô hình hóa các tương tác đặc trưng một cách tinh tế**. 

Bài báo nhận thấy rằng các phương pháp dự đoán CTR hiện tại thường có hai hạn chế chính. Thứ nhất, chúng thường **coi tất cả các đặc trưng có tầm quan trọng ngang nhau**, trong khi thực tế, một số đặc trưng (chẳng hạn như loại người dùng hoặc danh mục sản phẩm) có thể quan trọng hơn rất nhiều so với các đặc trưng khác. Thứ hai, việc mô hình hóa các tương tác đặc trưng thường được thực hiện bằng các phép tính đơn giản (như tích Hadamard hoặc tích vô hướng), nhưng những tương tác thực tế giữa các đặc trưng có thể phức tạp hơn nhiều và cần những phương pháp mô hình hóa tinh tế hơn.

Khoảng trống nghiên cứu mà FiBiNET nhằm lấp đầu là: **làm cách nào để động học (dynamically learn) tầm quan trọng của từng đặc trưng và đồng thời mô hình hóa các tương tác đặc trưng một cách tinh tế với khả năng biểu diễn cao?** FiBiNET đề xuất một kiến trúc kết hợp hai cơ chế: **(1) Squeeze-Excitation Network (SENET) để học tầm quan trọng đặc trưng** và **(2) các hàm song tuyến (bilinear functions) để mô hình hóa các tương tác đặc trưng phức tạp**.

## 2. Phương pháp sử dụng

**Kiến trúc tổng quan:** FiBiNET được thiết kế với hai biến thể - biến thể cạn (shallow) và biến thể sâu (deep) - nhưng cả hai đều chia sẻ những thành phần cốt lõi giống nhau.

**Thành phần 1 - Feature Embedding & Concatenation:**
Tất cả các đặc trưng đầu vào, bao gồm cả số và danh mục, được nhúng vào một không gian có chiều thấp (embedding space). Sau đó, tất cả các embedding này được nối (concatenate) lại để tạo thành một vector biểu diễn tổng hợp.

**Thành phần 2 - Feature Importance Learning via SENET (Học tầm quan trọng đặc trưng):**
Đây là phần sáng tạo nhất của FiBiNET. SENET (Squeeze-Excitation Network) là một cơ chế được phát triển ban đầu trong lĩnh vực thị giác máy tính (computer vision) để học được trọng số kênh (channel weights). FiBiNET áp dụng ý tưởng này cho các đặc trưng:

- **Squeeze (Nén):** Một phép toán nén giảm chiều của từng embedding đặc trưng thành một số vô hướng duy nhất, biểu diễn tầm quan trọng "tổng thể" của đặc trưng đó.

- **Excitation (Kích thích):** Một mạng nơ-ron nhỏ (thường là hai tầng fully-connected) được áp dụng lên các số vô hướng này để học được **trọng số tầm quan trọng (importance weights)** của từng đặc trưng. Những trọng số này là động - chúng không phải là hằng số mà được học từ dữ liệu.

- **Scale (Tỷ lệ):** Các embedding đặc trưng gốc được nhân với các trọng số tầm quan trọng tương ứng, có hiệu ứng là **"khuếch đại" những đặc trưng quan trọng và "làm yếu" những đặc trưng kém quan trọng**.

Cơ chế SENET này cho phép mô hình tự động học được tầm quan trọng tương đối của các đặc trưng, thay vì yêu cầu bước tiền xử lý thủ công. Điều này đặc biệt hữu ích vì tầm quan trọng đặc trưng có thể khác nhau tùy theo bối cảnh hoặc tập dữ liệu.

**Thành phần 3 - Bilinear Feature Interaction (Tương tác đặc trưng song tuyến):**
Sau khi đã được cân nhân bằng SENET, các embedding đặc trưng được đưa vào thành phần tương tác bilinear:

- **Hàm Bilinear:** Thay vì sử dụng các phép tính tương tác đơn giản (như tích Hadamard $\odot$ hay inner product $\langle \cdot, \cdot \rangle$), FiBiNET sử dụng **hàm bilinear** có dạng: $$\text{Bilinear}(x_i, x_j) = x_i^T W_{ij} x_j$$ trong đó $W_{ij}$ là ma trận trọng số học được cho cặp đặc trưng $(i, j)$. Phương pháp này mạnh mẽ hơn vì nó có khả năng mô hình hóa các tương tác **phi tuyến tính** giữa các đặc trưng.

- **Mở rộng lên tất cả cặp đặc trưng:** Bilinear interaction được tính cho tất cả các cặp đặc trưng, tạo ra một biểu diễn phong phú của các tương tác bậc hai. Mặc dù điều này có chi phí tính toán bậc hai ($O(n^2)$ trong số lượng đặc trưng), nhưng nó mang lại biểu diễn có khả năng biểu diễn cao hơn.

**Biến thể Shallow (Cạn):**
FiBiNET cạn bao gồm phần SENET + Bilinear interaction, tiếp theo là một tầng fully-connected duy nhất trước tầng output. Mô hình này tương đương về mặt khái niệm với Factorization Machines nhưng với sự cải thiện từ SENET.

**Biến thể Deep (Sâu):**
FiBiNET sâu kết hợp phần SENET + Bilinear interaction từ biến thể cạn, nhưng thay vì chỉ có một tầng fully-connected, nó thêm **các tầng học sâu (deep neural network layers)** để mô hình hóa các tương tác bậc cao hơn. Điều này cho phép mô hình kết hợp được cả những tương tác bậc hai được mô hình hóa tường minh bằng bilinear function và những tương tác bậc cao được mô hình hóa ẩn bằng các tầng DNN.

## 3. Thành tựu đạt được

FiBiNET được đánh giá trên **hai tập dữ liệu lớn và công khai**: Criteo và Avazu. Các kết quả cho thấy những cải thiện nhất quán so với các phương pháp cơ sở (baselines).

**Kết quả Biến thể Shallow:**
- **Outperforms FM (Factorization Machines):** FiBiNET cạn vượt trội hơn FM trong cả hai số liệu AUC và Logloss trên cả hai tập dữ liệu.
- **Outperforms FFM (Field-aware FM):** Mặc dù FFM là một phiên bản nâng cao của FM có khả năng mô hình hóa các tương tác field-aware, FiBiNET vẫn đạt được hiệu suất tốt hơn nhờ vào SENET và bilinear functions.

Kết quả này chứng minh rằng việc tích hợp SENET để học tầm quan trọng đặc trưng cùng với bilinear interactions là một sự cải thiện vượt trội so với các phương pháp tương tác đặc trưng truyền thống.

**Kết quả Biến thể Deep:**
- **Outperforms DeepFM:** DeepFM là một mô hình tiên tiến kết hợp các tương tác tường minh (thông qua FM module) và ẩn (thông qua DNN). FiBiNET sâu vượt trội hơn DeepFM, cho thấy rằng việc sử dụng bilinear functions thay vì FM module để mô hình hóa tương tác tường minh là hiệu quả hơn.

- **Outperforms xDeepFM:** xDeepFM (Extreme Deep Factorization Machines) là một phiên bản tiên tiến hơn nữa của DeepFM sử dụng một "compressed interaction network" để mô hình hóa các tương tác bậc cao tường minh. Tuy nhiên, FiBiNET vẫn đạt được hiệu suất tốt hơn hoặc tương đương, cho thấy rằng cách tiếp cận của FiBiNET là có giá trị.

- **Độ cải thiện:** Những cải thiện này thường ở mức khoảng 0.1-0.3% AUC (tương ứng với 0.2-0.5% cải thiện Logloss), nhưng như đã đề cập, trong bối cảnh quảng cáo trực tuyến, những con số này có giá trị kinh tế đáng kể.

**Ý nghĩa của những kết quả này:**

1. **Tầm quan trọng của việc học tầm quan trọng đặc trưng động:** Kết quả cho thấy rằng không phải tất cả các đặc trưng đều bình đẳng, và việc cho phép mô hình động học được tầm quan trọng của từng đặc trưng (thông qua SENET) đem lại lợi ích thực tế.

2. **Bilinear functions tốt hơn các tương tác đơn giản:** Việc sử dụng bilinear functions thay vì các phép tính tương tác đơn giản (Hadamard product, inner product) cho phép mô hình hóa các tương tác phức tạp hơn.

3. **Sự cân bằng giữa tường minh và ẩn:** Biến thể sâu của FiBiNET chứng minh rằng việc kết hợp cả các tương tác tường minh (bilinear) và ẩn (DNN) là hiệu quả hơn so với chỉ có một trong hai.

## 4. Hạn chế

**Các hạn chế về kiến trúc và thiết kế:**

1. **Độ phức tạp tính toán bậc hai:** Bilinear interactions có độ phức tạp $O(n^2)$ tương ứng với số lượng đặc trưng. Đối với các tập dữ liệu có số lượng đặc trưng cực lớn (hàng triệu), điều này có thể trở thành một thắc mắc cổ chai tính toán. Bài báo không thảo luận chiến lược nào để xử lý tình huống này, chẳng hạn như low-rank approximation của các ma trận $W_{ij}$.

2. **Sự lựa chọn kiến trúc SENET chưa được lý giải** trong bối cảnh CTR prediction:** SENET được phát triển ban đầu cho computer vision. Mặc dù ứng dụng của nó vào CTR prediction là hợp lý, nhưng bài báo không thảo luận xem liệu có những cơ chế khác, được thiết kế đặc biệt cho dữ liệu danh mục, có thể hiệu quả hơn hay không.

3. **Thiếu phân tích độ nhạy tham số:** Bao nhiêu tầng hidden trong mạng excitation của SENET tốt nhất? Activation functions nào hoạt động tốt nhất? Bài báo không cung cấp các phân tích chi tiết về những câu hỏi này.

4. **Vấn đề khả năng mở rộng:** Mặc dù bài báo báo cáo kết quả trên Criteo và Avazu, nhưng không rõ mô hình hoạt động như thế nào trên những tập dữ liệu có cấu trúc khác nhau hoặc số lượng đặc trưng cực lớn.

**Các hạn chế từ quan điểm thực nghiệm:**

1. **Thiếu ablation studies chi tiết:** Bài báo không cung cấp ablation study để chứng minh rằng cả SENET và bilinear interactions đều cần thiết. Ví dụ, mô hình sử dụng bilinear interactions mà không có SENET hiệu suất như thế nào?

2. **Thiếu so sánh với các phương pháp feature importance khác:** Có những phương pháp khác để học tầm quan trọng đặc trưng (chẳng hạn như attention mechanisms). Bài báo không so sánh FiBiNET với các cách tiếp cận này.

3. **Số lượng tập dữ liệu hạn chế:** Chỉ hai tập dữ liệu được sử dụng trong đánh giá. Mở rộng đánh giá trên nhiều tập dữ liệu với đặc điểm khác nhau (different domains, different feature distributions) sẽ cung cấp bằng chứng thuyết phục hơn.

4. **Không có tương tác với chuyên gia miền:** Bài báo không thảo luận xem liệu các trọng số tầm quan trọng học được bằng SENET có thể được xác thực hoặc giải thích bằng kiến thức chuyên gia miền hay không.

**Các hạn chế về khả năng giải thích:**

1. **Khó giải thích SENET weights:** Mặc dù SENET cung cấp một cơ chế để học tầm quan trọng đặc trưng, nhưng không rõ liệu những trọng số này có tương ứng với những tầm quan trọng thực sự có ý nghĩa kinh doanh hay chỉ là các mẫu số học được từ dữ liệu huấn luyện.

2. **Bilinear functions khó giải thích hơn:** Những ma trận $W_{ij}$ trong bilinear functions không có ý nghĩa trực tiếp và khó để giải thích những gì chúng đang mô hình hóa.

**Hướng phát triển tương lai:**

1. **Tối ưu hóa tính toán:** Sử dụng low-rank factorization để giảm chi phí tính toán của bilinear interactions, hoặc phát triển các phương pháp sparse interactions để chỉ tính toán những tương tác quan trọng nhất.

2. **Kết hợp với các phương pháp khác:** Thử nghiệm kết hợp FiBiNET với các phương pháp mô hình hóa tương tác khác (attention mechanisms, graph neural networks) để tạo ra các kiến trúc hybrid mạnh mẽ hơn.

3. **Cải thiện khả năng giải thích:** Phát triển các phương pháp để giải thích những gì SENET và bilinear functions đã học được, có thể thông qua sự kết hợp với các phương pháp explainability như SHAP hoặc integrated gradients.

4. **Phát triển các phương pháp feature importance được thiết kế đặc biệt:** Thay vì "mượn" SENET từ computer vision, phát triển những cơ chế feature importance được thiết kế đặc biệt cho bối cảnh CTR prediction với các đặc trưng danh mục thưa thớt.

5. **Mở rộng đánh giá:** Tiến hành những thử nghiệm trên các tập dữ liệu khác nhau, bao gồm cả những tập dữ liệu có cấu trúc khác biệt, để đánh giá khả năng tổng quát hóa (generalization) của FiBiNET.

