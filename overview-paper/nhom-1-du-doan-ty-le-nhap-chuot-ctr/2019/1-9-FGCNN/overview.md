# Review Paper: FGCNN - Feature Generation by Convolutional Neural Network for CTR Prediction

**ArXiv ID:** [1904.04447](https://arxiv.org/abs/1904.04447)  
**Năm:** 2019  
**Venue:** TheWebConf 2019  
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)

---

## 1. Paper này đang nghiên cứu gì?

FGCNN tập trung vào một thách thức cốt lõi trong dự đoán CTR: **làm thế nào để tự động sinh ra các đặc trưng tương tác có ý nghĩa mà không cần can thiệp thủ công của chuyên gia?** Bài báo nhận thấy rằng mặc dù các mạng nơ-ron sâu (Deep Neural Networks - DNNs) có khả năng học được các tương tác đặc trưng, nhưng **"những tương tác hữu ích luôn luôn thưa thớt"** - điều này khiến cho DNN phải sử dụng một lượng lớn tham số để học được những tương tác thưa thớt này, dẫn đến hiện tượng quá khớp (overfitting) và học kém hiệu quả.

Mặt khác, kỹ thuật kỹ thuật đặc trưng thủ công (manual feature engineering) có thể cải thiện hiệu suất đáng kể, nhưng nó đòi hỏi **kiến thức chuyên sâu về miền và rất tốn thời gian**. Hơn nữa, việc xây dựng các đặc trưng thủ công cho một tập dữ liệu không thể được tái sử dụng trực tiếp cho tập dữ liệu khác hoặc các tình huống kinh doanh khác.

Khoảng trống nghiên cứu mà FGCNN nhằm lấp đầy là: **làm cách nào để tự động sinh ra (generate) các đặc trưng mới có ý nghĩa từ những đặc trưng gốc, giảm gánh nặng học tập của DNN, đồng thời tránh cần thiết phải có kiến thức chuyên gia?** FGCNN đề xuất sử dụng **Convolutional Neural Networks (CNNs)** - một kiến trúc được thiết kế để phát hiện các mẫu cục bộ (local patterns) trong dữ liệu - để tự động sinh ra các đặc trưng tương tác mới.

## 2. Phương pháp sử dụng

**Kiến trúc hai thành phần:** FGCNN bao gồm hai phần chính được thiết kế để làm việc với nhau một cách hiệu quả.

**Thành phần 1 - Feature Generation (Sinh tạo đặc trưng):**
Đây là phần cốt lõi của FGCNN. Bài báo sử dụng CNNs với một cách tiếp cận sáng tạo:

- **Ánh xạ đặc trưng thành ma trận:** Trước tiên, các đặc trưng đầu vào được nhúng vào một không gian thấp chiều, tạo thành một ma trận đặc trưng nhúng (feature embedding matrix).

- **Áp dụng Convolution:** Các bộ lọc (filters) CNN được áp dụng lên ma trận này với các kích thước cửa sổ (kernel sizes) khác nhau để phát hiện các **mẫu cục bộ và tương tác cục bộ** giữa các đặc trưng. Mỗi bộ lọc học được một kiểu tương tác cụ thể. Ví dụ, một bộ lọc có thể học được tương tác giữa một cặp đặc trưng, bộ lọc khác có thể học được tương tác giữa ba đặc trưng liên tiếp, v.v.

- **Tái kết hợp (Recombination):** Sau đó, các kết quả từ các bộ lọc khác nhau được **tái kết hợp để sinh ra các đặc trưng mới**. Những đặc trưng sinh ra này không chỉ là các tương tác tuyến tính đơn giản, mà là những biểu diễn phức tạp hơn của các mẫu cục bộ được CNN phát hiện.

Cách tiếp cận này có một ưu điểm cực kỳ quan trọng: thay vì yêu cầu DNN học được các tương tác từ không gian đặc trưng gốc quá lớn, CNN đã "chuẩn bị" sẵn một không gian đặc trưng được làm giàu (enriched feature space) chứa các đặc trưng tương tác có ý nghĩa. Điều này **giảm gánh nặng học tập** của phần phân loại, cho phép nó tập trung vào việc học các quyết định phân loại thay vì học các tương tác từ đầu.

**Thành phần 2 - Deep Classifier (Phân loại học sâu):**
Phần này sử dụng **kiến trúc IPNN (Inner Product Neural Network)** để học được các tương tác từ không gian đặc trưng được làm giàu. IPNN là một phương pháp được thiết kế đặc biệt để mô hình hóa các tương tác đặc trưng thông qua các phép tính tích vô hướng (inner products).

Một trong những thiết kế thông minh nhất của FGCNN là tính **modular** của nó: mặc dù bài báo sử dụng IPNN làm phân loại, nhưng về mặt lý thuyết, bất kỳ kiến trúc phân loại nào (DeepFM, xDeepFM, DeepNeuralNetwork, v.v.) cũng có thể được sử dụng. Điều này cho phép linh hoạt lớn và khả năng tích hợp với các mô hình tiên tiến khác.

**Quy trình huấn luyện end-to-end:**
Toàn bộ mô hình (CNN + Classifier) được huấn luyện một cách kết thúc đến kết thúc (end-to-end) bằng cách tối thiểu hóa hàm mất mát nhị phân (binary cross-entropy loss) trên dữ liệu huấn luyện.

## 3. Thành tựu đạt được

FGCNN được đánh giá trên **ba tập dữ liệu quy mô lớn**: Criteo, Avazu, và Huawei App Store. Các kết quả cho thấy những cải thiện đáng kể và nhất quán.

**Kết quả so sánh với IPNN (phân loại được sử dụng trong FGCNN):**
- **Criteo dataset:** Cải thiện AUC **0.11%** (tương ứng với 0.2% cải thiện Logloss)
- **Avazu dataset:** Cải thiện AUC **0.19%** (tương ứng với 0.29% cải thiện Logloss)
- **Huawei App Store dataset:** Cải thiện AUC **0.13%** (tương ứng với 0.79% cải thiện Logloss)

Những con số này có vẻ nhỏ, nhưng trong ngành công nghiệp quảng cáo trực tuyến, thậm chí những cải thiện 0.1% AUC cũng có giá trị lớn, tương ứng với hàng triệu đô la doanh thu.

**So sánh với các phương pháp cơ sở (baselines):**
FGCNN **vượt trội hơn tất cả 9 mô hình so sánh**, bao gồm:
- **Mô hình không thần kinh:** Logistic Regression (LR), Gradient Boosting Decision Trees (GBDT), Factorization Machines (FM), Field-aware Factorization Machines (FFM)
- **Mô hình học sâu tiên tiến:** DeepFM, xDeepFM, IPNN, PIN (Product-based Interaction Networks)

**Ý nghĩa của những cải thiện này:**
Kết quả cho thấy rằng việc sinh ra các đặc trưng tương tác một cách tự động bằng CNN không chỉ có hiệu quả hơn so với để phân loại tự học các tương tác từ đầu, mà còn cho phép các kiến trúc phân loại khác nhau hoạt động tốt hơn. Điều này gợi ý rằng **cơ chế sinh tạo đặc trưng của FGCNN đã khám phá ra một không gian đặc trưng được chọn lọc kỹ lưỡng** mà có giá trị nội tại cho bài toán dự đoán CTR.

## 4. Hạn chế

**Các hạn chế về kiến trúc và thiết kế:**

1. **Độ phức tạp tính toán chưa được phân tích rõ ràng:** Bài báo không cung cấp chi tiết về chi phí tính toán của phần sinh tạo đặc trưng bằng CNN. Khi áp dụng các bộ lọc CNN với các kích thước khác nhau và tái kết hợp, độ phức tạp có thể tăng đáng kể so với các phương pháp truyền thống, nhưng bài báo không thảo luận chi tiết về vấn đề này.

2. **Sự lựa chọn tham số CNN không có hướng dẫn rõ ràng:** Bao nhiêu bộ lọc? Kích thước bộ lọc nào tốt nhất? Làm cách nào để chọn các siêu tham số CNN cho một tập dữ liệu mới? Bài báo không cung cấp hướng dẫn chi tiết về những câu hỏi này, làm cho việc áp dụng FGCNN vào các tập dữ liệu mới trở nên khó khăn.

3. **Thiếu phân tích độ nhạy tham số:** Không có nghiên cứu về cách các siêu tham số CNN (số lượng bộ lọc, kích thước bộ lọc, activation functions) ảnh hưởng đến hiệu suất cuối cùng.

4. **Khả năng giải thích bị giảm:** Mặc dù FGCNN cải thiện hiệu suất, nhưng việc sinh ra các đặc trưng mới qua CNN làm cho mô hình trở nên **kém dễ giải thích** hơn so với các phương pháp feature engineering truyền thống. Các đặc trưng sinh ra có thể không có ý nghĩa kinh doanh rõ ràng.

**Hạn chế từ quan điểm thực nghiệm:**

1. **Tập dữ liệu thử nghiệm hạn chế:** Bài báo chỉ đánh giá trên ba tập dữ liệu. Mặc dù đây là những tập dữ liệu quy mô lớn và phổ biến, nhưng việc mở rộng đánh giá trên nhiều tập dữ liệu khác nhau với đặc điểm khác nhau sẽ cung cấp bằng chứng thuyết phục hơn.

2. **Thiếu tương tác trực tiếp với chuyên gia miền:** Bài báo không thảo luận xem liệu các đặc trưng sinh ra có thể được xác thực hoặc cải thiện bằng kiến thức chuyên gia miền hay không.

**Hướng phát triển tương lai:**

1. **Kết hợp CNN với các kỹ thuật khác:** Thay vì chỉ sử dụng CNN, có thể kết hợp CNN với các phương pháp phát hiện mẫu khác (RNNs, Graph Neural Networks) để sinh ra các đặc trưng đa dạng hơn.

2. **Tự động chọn kiến trúc CNN:** Sử dụng Neural Architecture Search (NAS) để tự động tìm ra cấu hình CNN tối ưu cho một tập dữ liệu cho trước.

3. **Cải thiện khả năng giải thích:** Phát triển các phương pháp để giải thích những gì các bộ lọc CNN đã học được, có thể thông qua sự kết hợp với các phương pháp explainability như LIME hoặc SHAP.

4. **Tối ưu hóa tính toán:** Tìm cách giảm chi phí tính toán của phần CNN, chẳng hạn thông qua việc sử dụng các kỹ thuật nén mô hình hoặc tính toán lượng tử hóa (quantization).

5. **Mở rộng cho các loại dữ liệu khác:** Thử nghiệm FGCNN trên các loại dữ liệu khác như dữ liệu thời gian (time series) hoặc dữ liệu đồ thị (graph data).

