# Review Paper: CAN: Feature Co-Action Network for Click-Through Rate Prediction

**ArXiv ID:** [2011.05625](https://arxiv.org/abs/2011.05625)
**Năm:** 2020
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)
**Tác giả:** Weijie Bian, Kailun Wu, và các cộng sự từ Alibaba và các tổ chức khác
**Liên hệ:** Guorui Zhou
**Hội nghị:** WSDM 2022

---

## 1. Paper này đang nghiên cứu gì?

Paper này giải quyết vấn đề cơ bản trong dự đoán CTR: cách mô hình hóa các tương tác đặc trưng (feature interactions) một cách hiệu quả. Đây là một vấn đề được công nhận rộng rãi: "Feature interaction has been recognized as an important problem in machine learning" - tương tác đặc trưng được công nhận là một vấn đề quan trọng trong học máy.

Vấn đề cốt lõi nằm ở giới hạn của các phương pháp hiện tại. Các mạng nơron sâu (Deep Neural Networks - DNNs) học các tương tác đặc trưng một cách "ẩn" (implicit) - chúng học các biểu diễn (representation) có khả năng nắm bắt các mối quan hệ giữa các đặc trưng, nhưng những mối quan hệ này không rõ ràng và khó giải thích. Điều này dẫn đến một hạn chế quan trọng: các tương tác ẩn này "cannot fully retain the complete representation capacity of the original and empirical feature interactions (e.g., cartesian product)" - không thể hoàn toàn giữ lại khả năng biểu diễn hoàn chỉnh của các tương tác đặc trưng gốc.

Để minh họa: một cartesian product của hai đặc trưng A và B sẽ tạo ra một không gian tương tác hoàn chỉnh với tất cả các tổ hợp có thể, nhưng phương pháp này không khả thi về mặt tính toán khi số lượng đặc trưng lớn. Các phương pháp factorization như Factorization Machines (FM) giảm bớt độ phức tạp nhưng mất mát thông tin.

Lỗ hổng nghiên cứu rõ ràng: không có phương pháp nào kết hợp:
- Khả năng nắm bắt đầy đủ các tương tác đặc trưng một cách rõ ràng
- Hiệu quả tính toán và tham số khả thi
- Hiệu suất thực tiễn trên các bộ dữ liệu công khai và công nghiệp

Động lực từ thực tiễn: Alibaba là một trong những công ty quảng cáo lớn nhất thế giới, nên việc cải tiến mô hình dự đoán CTR có tác động kinh doanh trực tiếp và đáng kể.

## 2. Phương pháp sử dụng

**Cơ chế Co-Action (Hành động kết hợp):** CAN giới thiệu một cách tiếp cận mới để mô hình hóa tương tác giữa từng cặp đặc trưng. Thay vì sử dụng các tương tác ẩn hoặc toán tử element-wise đơn giản, CAN định nghĩa tương tác giữa hai đặc trưng A và B như sau:

1. **Embedding của Đặc trưng A:** Đặc trưng A được biểu diễn dưới dạng một embedding vector (vectơ nhúng). Đây là một biểu diễn học được có khả năng nắm bắt đặc điểm quan trọng của đặc trưng A.

2. **MLP Đại diện cho Đặc trưng B:** Đặc trưng B không được biểu diễn trực tiếp dưới dạng embedding. Thay vào đó, một mạng Multi-Layer Perceptron (MLP) được huấn luyện để "đại diện" cho đặc trưng B. MLP này học cách biến đổi các đầu vào khác để phản ánh tác động của đặc trưng B.

3. **Tính toán Tương tác:** Tương tác giữa A và B được tính bằng cách "passing the embedding of feature A through feature B's MLP network" - truyền embedding của đặc trưng A qua mạng MLP của đặc trưng B. Phép toán này tạo ra một giá trị tương tác duy nhất cho cặp (A, B).

**Lý do đằng sau thiết kế này:** Phương pháp này cho phép:
- **Tính rõ ràng:** Mỗi tương tác pairwise được tính toán một cách rõ ràng, không ẩn trong các biểu diễn sâu
- **Linh hoạt:** MLP có khả năng học các hàm biến đổi phi tuyến phức tạp, cho phép nắm bắt các tương tác phức tạp
- **Hiệu quả tham số:** Thay vì một ma trận tương tác lớn cho tất cả các cặp đặc trưng, chúng ta sử dụng embedding và MLPs, giảm đáng kể số tham số

**Xử lý Toàn diện:** CAN xử lý:
- Các tương tác giữa tất cả các cặp đặc trưng (hoặc một tập con có ý nghĩa)
- Cả các đặc trưng categorical và numerical thông qua embeddings thích hợp
- Tích hợp các embedding cấp độ trường (field-level embeddings) từ các thành phần khác

**Kiến trúc Tổng hợp:** Paper không cung cấp chi tiết về cách tổng hợp tất cả các tương tác pairwise thành dự đoán cuối cùng, nhưng có thể:
- Tất cả các tương tác được cộng (sum pooling)
- Hoặc sử dụng một mạng tổng hợp để học cách kết hợp chúng
- Kết hợp với các đặc trưng bậc nhất (first-order features) để dự đoán cuối cùng

**Khả năng Mô hình Cao:** Bằng cách sử dụng các embedding và MLPs riêng biệt, CAN có khả năng mô hình cao - nó có thể biểu diễn một phạm vi rộng của các hàm tương tác mà không bị giới hạn bởi các cấu trúc đơn giản như FM.

## 3. Thành tựu đạt được

**Vượt trội trên Bộ dữ liệu Công khai:** CAN "outperformed state-of-the-art CTR models" trên cả bộ dữ liệu công khai (public datasets) và bộ dữ liệu công nghiệp (industrial datasets). Điều này chứng minh tính hiệu quả của phương pháp co-action trên các bộ dữ liệu đa dạng.

**So sánh với Cartesian Product Baselines:** Paper đặc biệt đáng chú ý vì nó so sánh CAN với các baseline dựa trên cartesian product, chứng minh rằng cách tiếp cận co-action của CAN "surpasses factorization machine (FM)-based models and their variations" - vượt trội các mô hình dựa trên Factorization Machine và các biến thể của chúng. Điều này có nghĩa CAN nắm bắt được các tương tác phức tạp mà FM không thể.

**Triển khai Thực tiễn tại Alibaba:** Kết quả ấn tượng nhất đến từ triển khai thực tế trên hệ thống quảng cáo hiển thị (display advertising system) của Alibaba:
- **12% improvement in CTR** - cải tiến 12% trong tỷ lệ nhấp chuột, một con số rất lớn trong lĩnh vực này
- **8% improvement in Revenue Per Mille (RPM)** - cải tiến 8% trong doanh thu mỗi nghìn lần hiển thị

Những con số này chứng minh rằng cải tiến không chỉ là kỹ thuật mà còn có tác động kinh doanh trực tiếp đáng kể.

**Hiệu quả Tham số:** Mặc dù paper không công bố con số cụ thể, nó được thiết kế để "balance model capacity with parameter efficiency" - cân bằng khả năng mô hình với hiệu quả tham số. Điều này có nghĩa là CAN đạt được kết quả tốt hơn mà không cần số lượng tham số quá lớn so với các phương pháp khác.

**Giải pháp Thực tiễn:** CAN được mô tả là "offering a practical solution for real-world recommendation systems" - cung cấp một giải pháp thực tiễn cho các hệ thống gợi ý thế giới thực. Điều này có nghĩa nó không chỉ tốt trên giấy mà còn dễ triển khai và duy trì trong sản xuất.

**Công bố Hội nghị Hàng Đầu:** Công bố tại WSDM 2022 (Web Search and Data Mining) cho thấy công trình được cộng đồng nghiên cứu công nhận rộng rãi.

## 4. Hạn chế

**Thiếu Chi tiết Kiến trúc Cụ thể:** Paper không cung cấp đủ chi tiết về:
- Chính xác cách các embedding được khởi tạo và học
- Cấu trúc chi tiết của các MLPs đại diện cho mỗi đặc trưng
- Cách tối ưu hóa các tương tác khi số lượng đặc trưng lớn

Thiếu sót này hạn chế khả năng tái tạo hoàn toàn từ mô tả paper.

**Độ phức tạp Tính toán:** Mặc dù được tuyên bố là "hiệu quả tham số", không rõ độ phức tạp thời gian của việc tính tất cả các tương tác pairwise, đặc biệt với hàng trăm hoặc hàng nghìn đặc trưng. Việc này có thể trở thành nút cổ chai hiệu suất.

**Không có Ablation Study Chi tiết:** Paper không cung cấp nghiên cứu loại bỏ từng thành phần (ablation study) để xác định:
- Đóng góp của embeddings so với MLPs
- Tác động của sử dụng MLP vs các hàm biến đổi khác
- Tương tác nào (pairwise vs higher-order) là quan trọng nhất

**Khách quát hóa Giữa các Miền:** Kết quả chủ yếu được báo cáo trong bối cảnh quảng cáo Alibaba. Không rõ CAN khái quát hóa tốt như thế nào đến:
- Các nền tảng quảng cáo khác với đặc điểm dữ liệu khác
- Các ứng dụng khác như gợi ý sản phẩm, xếp hạng tìm kiếm
- Các bộ dữ liệu công khai khác ngoài những cái được kiểm tra

**Không So Sánh với Một Số Phương Pháp Mới:** Paper không so sánh với một số phương pháp mô hình hóa tương tác khác có thể:
- Sử dụng attention mechanisms
- Sử dụng graph neural networks
- Sử dụng các phương pháp kernel khác

**Độ Phức tạp của Mô hình:** CAN đưa ra thêm một lớp phức tạp - cần phải định nghĩa và học một MLP cho mỗi đặc trưng. Điều này có thể làm cho việc hiệp chỉnh và triển khai khó khăn hơn so với các mô hình đơn giản hơn.

**Hướng Tương lai:** Paper gợi ý cơ hội:
- Mở rộng đến các tương tác bậc cao hơn (higher-order interactions)
- Cải tiến cơ chế tổng hợp của các tương tác
- Tích hợp tốt hơn với các thành phần gating hoặc attention khác

---

**Đóng góp chính:** CAN giới thiệu cơ chế co-action để mô hình hóa các tương tác đặc trưng một cách rõ ràng và hiệu quả, chứng minh rằng cách tiếp cận này vượt trội các phương pháp factorization truyền thống trên cả bộ dữ liệu công khai (outperforming baselines) và triển khai thực tế (12% CTR, 8% RPM improvement tại Alibaba).
