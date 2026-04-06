# Review Paper: Graph Factorization Machines for CTR Prediction

**ArXiv ID:** [2105.11866](https://arxiv.org/abs/2105.11866)
**Năm:** 2021
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)

---

## 1. Paper này đang nghiên cứu gì?

GraphFM (Graph Factorization Machines) tập trung vào việc cải thiện Factorization Machines (FM) - một trong những mô hình cơ bản và hiệu quả nhất trong CTR prediction - bằng cách kết hợp chúng với Graph Neural Networks (GNNs). Vấn đề cốt lõi mà paper giải quyết là những **hạn chế cơ bản của Factorization Machines truyền thống**.

FM truyền thống được thiết kế để mô phỏng tương tác feature **bậc hai (pairwise interactions)**, nhưng chúng **không thể nắm bắt tương tác bậc cao (higher-order interactions)** một cách hiệu quả. Sự mở rộng tự nhiên để mô phỏng các tương tác bậc cao sẽ gặp phải **vấn đề kỳ vọng kết hợp (combinatorial explosion)** - số lượng các tương tác có thể tăng theo hàm mũ, làm cho việc tính toán trở nên không khả thi.

Ngoài ra, FM truyền thống xem xét **tất cả các cặp feature** như những tương tác tiềm năng. Điều này có một hậu quả không mong muốn: nó **đưa vào nhiều noise** từ những cặp feature không liên quan mà nếu được coi là tương tác sẽ làm giảm chất lượng dự đoán. Không phải tất cả các feature pairs đều có ý nghĩa tương tác - một số cặp đơn giản không ảnh hưởng đến nhau, nhưng FM truyền thống vẫn cố gắng mô phỏng tương tác của chúng.

Bối cảnh của paper là một xu hướng lớn trong cộng đồng học máy: **sử dụng Graph Neural Networks để mô phỏng dữ liệu và mối quan hệ phức tạp**. Paper gợi ý rằng có thể áp dụng các ý tưởng từ GNNs vào việc cải thiện Factorization Machines.

Motivation chính là **khắc phục hai hạn chế này đồng thời**: (1) mở rộng FM để mô phỏng tương tác bậc cao mà không gặp phải combinatorial explosion, và (2) lựa chọn một cách thông minh những tương tác feature nào là có ích, từ đó loại bỏ noise từ những cặp không liên quan.

## 2. Phương pháp sử dụng

GraphFM giới thiệu một cách tiếp cận hoàn toàn mới bằng cách **biểu diễn features dưới dạng một đồ thị (graph structure)**:

**Xây Dựng Đồ Thị Feature:** Thay vì xem features như một tập hợp độc lập, GraphFM biểu diễn chúng như các **node (nút)** trong một đồ thị. Điều này tạo nên một không gian mới để suy nghĩ về mối quan hệ giữa các features. Ban đầu, không có edges (cạnh) nào, nhưng chúng sẽ được xây dựng dựa trên tương tác.

**Cơ Chế Lựa Chọn Tương Tác (Interaction Selection):** Paper thiết kế một **cơ chế thông minh để chọn lựa những tương tác feature nào là có giá trị** và nên được biểu diễn là edges trong đồ thị. Điều này hoạt động như sau:

1. Cho mỗi cặp feature i và j, mô hình tính toán một **metric score** để đánh giá liệu tương tác giữa chúng có giá trị hay không
2. Metric này được tính bằng cách sử dụng một **Multi-Layer Perceptron (MLP) với một hidden layer**
3. MLP nhận đầu vào là **element-wise product (tích từng phần tử)** của các feature vectors i và j
4. Output là một **scalar continuous score** (điểm liên tục từ 0 đến 1), biểu diễn xác suất (hoặc độ mạnh) của tương tác

Điểm số này cho phép gradient-based optimization, nghĩa là mô hình có thể học được những tương tác nào là quan trọng thông qua quá trình backpropagation thông thường.

**Động Cơ của Cấu Trúc Đồ Thị:** Một đặc điểm quan trọng là **cấu trúc đồ thị được học lại tại mỗi lớp (layer)** của kiến trúc. Điều này có nghĩa là:
- Layer đầu tiên có thể khám phá các tương tác bậc 2 (pairwise)
- Layer thứ hai có thể khám phá các tương tác bậc 3 (giữa các feature và các tương tác từ layer trước)
- Và cứ thế tiếp tục

Cấp độ linh hoạt này cho phép mô hình tự động khám phá những tương tác bậc cao nào là có ích mà không cần định tính sẵn chúng.

**Tích Hợp GNN Aggregation với FM Interactions:** GraphFM **kết hợp phép toán tương tác của Factorization Machines với chiến lược aggregation của Graph Neural Networks**. Cụ thể:

1. Thay vì chỉ aggregating các feature embeddings của các hàng xóm (như GNN tiêu chuẩn), GraphFM aggregates **các tương tác (element-wise products)** của các feature embeddings
2. Quá trình aggregation sử dụng các **learnable projection vectors** và **LeakyReLU non-linear activation functions**
3. Điều này tạo ra các **attention coefficients** để xác định tầm quan trọng (weights) của các tương tác khác nhau

**Multi-Head Attention trong GNN Aggregation:** Paper sử dụng **multi-head attention mechanisms** để nắm bắt "diverse polysemy of feature interactions in different semantic subspaces." Điều này có nghĩa là:
- Không chỉ có một cách để aggregating các tương tác
- Mô hình tìm hiểu nhiều cách khác nhau (different heads) để xem xét những tương tác nào là quan trọng
- Các heads này tương ứng với những khía cạnh khác nhau của dữ liệu

**Cập Nhật Feature Representations:** Biểu diễn feature mới ở mỗi layer kết hợp **cả soft attention** (từ attention mechanism) **và hard attention** (từ interaction selection mechanism). Điều này cho phép:
- Những tương tác được chọn (hard selection) được coi là quan trọng
- Trong những tương tác được chọn đó, một số được áp dụng nhiều hơn dựa trên attention weights (soft weighting)

**Xếp Chồng (Stacking) các Layers:** Để mô phỏng các tương tác bậc cao tùy ý, kiến trúc xếp chồng nhiều lớp GraphFM. Mỗi lớp nhận đầu vào từ lớp trước, xây dựng lại cấu trúc đồ thị, chọn lựa tương tác, và tạo ra những biểu diễn mới. Quá trình này có thể lặp lại nhiều lần để nắm bắt những tương tác bậc cao tùy ý.

## 3. Thành tựu đạt được

GraphFM được đánh giá toàn diện trên các **bộ dữ liệu benchmark CTR tiêu chuẩn** cũng như **các bộ dữ liệu hệ thống khuyến nghị (recommender system datasets)** để chứng minh tính khái quát hóa (generalization) của phương pháp.

**Cải Thiện Hiệu Suất Trên Dữ Liệu CTR:**
- **Criteo Dataset:** GraphFM đạt AUC của 0.8091, vượt qua các baseline mạnh như:
  - AutoInt: 0.8084
  - Fi-GNN: 0.8077
- **MovieLens-1M Dataset:** GraphFM đạt AUC của 0.8902, vượt qua:
  - AutoInt: 0.8823
  - Fi-GNN: 0.8792

**Mức Độ Cải Thiện:** Các cải thiện được báo cáo là **ở mức 0.001 (at the 0.001-level)** trên các bộ dữ liệu CTR. Mặc dù con số này có vẻ nhỏ, nhưng trong lĩnh vực CTR prediction, ngay cả những cải thiện 0.0001 cũng được coi là có ý nghĩa tại scale của những hệ thống quảng cáo lớn (với hàng tỷ impressions mỗi ngày, ngay cả cải thiện nhỏ dẫn đến tăng doanh thu đáng kể).

**Ablation Studies (Nghiên Cứu Loại Bỏ Thành Phần):** Paper tiến hành các ablation studies chi tiết để đánh giá đóng góp của mỗi thành phần:
- **Interaction Selection Mechanism:** Được chứng minh là rất quan trọng - loại bỏ nó làm giảm hiệu suất đáng kể
- **Multi-Head Attention:** Cũng là một thành phần quan trọng, chứng minh rằng việc xem xét nhiều khía cạnh của tương tác là cần thiết
- Tất cả các thành phần đều **đóng góp có ý nghĩa (meaningful contribution)** vào hiệu suất tổng thể

**Tính Khả Diễn Giải:** GraphFM cung cấp khả năng diễn giải tốt hơn so với các black-box models:
- Có thể kiểm tra cấu trúc đồ thị được học để hiểu những tương tác nào được mô hình coi là quan trọng
- Có thể phân tích attention weights để thấy làm thế nào các tương tác này ảnh hưởng đến dự đoán

**Khái Quát Hóa Trên Các Loại Dữ Liệu:** Thực tế là GraphFM hoạt động tốt trên cả dữ liệu CTR (quảng cáo) và dữ liệu recommender system cho thấy phương pháp có khả năng khái quát hóa tốt trên các loại ứng dụng khác nhau.

## 4. Hạn chế

Mặc dù GraphFM là một đóng góp đáng kể cho lĩnh vực CTR prediction, paper vẫn có những hạn chế:

**Độ Phức Tạp Tính Toán:** Việc xây dựng đồ thị tại mỗi layer, tính toán interaction selection scores cho tất cả các cặp features, và thực hiện GNN aggregation đều có chi phí tính toán. Với hàng triệu features trong các ứng dụng thực tế, chi phí này có thể trở nên đáng kể. Paper không cung cấp một phân tích chi tiết về độ phức tạp tính toán so với các baseline.

**Khả Năng Mở Rộng (Scalability):** Liệu GraphFM có thể mở rộng đến các bộ dữ liệu với số lượng features rất lớn hay không? Với n features, có O(n²) cặp tiềm năng để xem xét. Mặc dù interaction selection giúp loại bỏ những cặp không quan trọng, nhưng ban đầu vẫn cần tính toán một số lượng lớn các scores.

**Lựa Chọn Hyperparameter:** Cấu trúc đồ thị được học, nhưng vẫn có các hyperparameters khác cần tuning:
- Số lượng layers
- Kích thước của MLPs trong interaction selection
- Số heads trong multi-head attention
- Ngưỡng (threshold) để chọn edges (nếu có)

Paper không chi tiết hóa đủ về việc làm thế nào để tuning những hyperparameters này một cách hiệu quả.

**Phân Tích Chi Tiết Về Tương Tác Được Học:** Mặc dù paper nhấn mạnh khả năng diễn giải, nó không cung cấp phân tích sâu về **những tương tác nào thực sự được mô hình học**. Có phải những tương tác được chọn là những tương tác mà các domain experts sẽ chọn không? Liệu chúng có khớp với intuition về feature engineering không?

**Mở Rộng Đến Các Loại Dữ Liệu Khác:** Đánh giá chủ yếu tập trung vào dữ liệu quảng cáo thưa thớt và recommender systems. Hiệu quả trên các loại dữ liệu hoàn toàn khác (ví dụ: dense features, dữ liệu văn bản, dữ liệu hình ảnh) chưa được khám phá.

**So Sánh Công Bằng:** Có vấn đề tiềm năng về công bằng trong so sánh: GraphFM có thể có số lượng tham số (parameters) khác so với các baseline. Các so sánh giữa các mô hình có cùng số lượng tham số sẽ giúp làm rõ ràng liệu cải thiện là do cơ chế của GraphFM hay do tăng độ phức tạp của mô hình.

**Hướng Nghiên Cứu Tương Lai:** Paper gợi ý những hướng phát triển như:
- Khám phá các cơ chế interaction selection hiệu quả hơn để xử lý các bộ dữ liệu lớn
- Phân tích kỹ lưỡng hơn về các tương tác được học
- Mở rộng phương pháp đến các loại dữ liệu và ứng dụng khác
- Tối ưu hóa các hyperparameters một cách tự động

---

## Tham Khảo

- [GraphFM - ArXiv 2105.11866](https://arxiv.org/abs/2105.11866)
- [GraphFM - HTML Version](https://arxiv.org/html/2105.11866)
- [GraphFM - Machine Intelligence Research (Published)](https://link.springer.com/article/10.1007/s11633-024-1505-5)
- [GraphFM - GitHub Repository](https://github.com/CRIPAC-DIG/GraphCTR)
- [GraphFM - ADS Abstract](https://ui.adsabs.harvard.edu/abs/2021arXiv210511866W/abstract)
