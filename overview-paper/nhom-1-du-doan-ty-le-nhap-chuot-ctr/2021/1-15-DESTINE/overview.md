# Review Paper: Disentangled Self-Attentive Neural Networks for CTR Prediction

**ArXiv ID:** [2101.03654](https://arxiv.org/abs/2101.03654)
**Năm:** 2021
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR)

---

## 1. Paper này đang nghiên cứu gì?

DESTINE (DisentanglEd Self-atTentIve NEtwork) tập trung vào bài toán dự đoán tỷ lệ nhấp chuột (Click-Through Rate - CTR) trong các ứng dụng quảng cáo trực tuyến. Vấn đề cốt lõi mà paper này giải quyết là các mô hình self-attention truyền thống trong CTR prediction có sự kết hợp chặt chẽ (coupling) giữa hai thành phần quan trọng: *unary term* (mô phỏng tầm quan trọng chung của một feature đối với tất cả các feature khác) và *pairwise interaction term* (mô phỏng tác động thuần túy của từng cặp feature). Sự kết hợp này dẫn đến việc tính gradient bị chia sẻ (coupled gradient computation) và sử dụng chung các phép biến đổi (shared transformations), gây trở ngại cho việc học hiệu quả cả hai thành phần.

Trong bối cảnh dữ liệu quảng cáo có chiều cao và thưa thớt (high-dimensional sparse data), việc mô phỏng chính xác các tương tác feature bậc cao là vô cùng quan trọng. Các phương pháp trước đây như AutoInt sử dụng self-attention nhưng không tách biệt rõ ràng hai loại tương tác này, dẫn đến hiệu suất không tối ưu. Paper chỉ ra rằng khóa để dự đoán hiệu quả là mô phỏng chính xác tương tác feature bậc cao, nhưng điều này đòi hỏi phải tách biệt và xử lý độc lập các thành phần khác nhau của self-attention mechanism.

Motivation chính là cải thiện khả năng học của mô hình bằng cách loại bỏ sự kết hợp chặt chẽ, cho phép mỗi thành phần (unary và pairwise) được tối ưu hóa riêng biệt với gradient và transformations của riêng chúng. Điều này dẫn đến hiệu suất cao hơn trong khi vẫn duy trì tính hiệu quả tính toán.

## 2. Phương pháp sử dụng

DESTINE sử dụng kiến trúc mạng thần kinh dựa trên self-attention được tách rời, được thiết kế để xử lý dữ liệu CTR thưa thớt và cao chiều. Bước đầu tiên là nhúng (embedding) các feature đầu vào thành các vector biểu diễn. Thay vì sử dụng self-attention tiêu chuẩn như AutoInt, DESTINE tách rõ ràng phép tính self-attention thành hai phần độc lập:

**Phần Unary Term:** Thành phần này mô phỏng tầm quan trọng chung của mỗi feature. Nó được tính toán thông qua một đường dẫn riêng (separate pathway) với các ma trận biến đổi riêng của nó. Cách tiếp cận này cho phép mô hình học cách một feature ảnh hưởng đến tất cả các feature khác một cách độc lập với các tương tác cặp.

**Phần Pairwise Interaction Term:** Phần này tập trung vào việc mô hỏa tác động thuần túy của từng cặp feature. Nó sử dụng phép tích trong (inner product) giữa các embedding feature để tính toán điểm tương tác (interaction score) giữa các cặp feature. Tác động thuần túy này bổ sung (complement) các vấn đề mà unary term không thể nắm bắt.

Kiến trúc sử dụng **multi-head attention**: mỗi attention head tập trung vào các khía cạnh khác nhau của mối quan hệ feature, cho phép mô hình học những tương tác phức tạp và đa dạng. Các head này hoạt động song song, mỗi cái có trọng số attention riêng. Kết quả từ các head được kết hợp để thu được biểu diễn tương tác hoàn chỉnh.

Để mô phỏng các tương tác feature bậc cao (higher-order interactions), paper xếp chồng nhiều lớp self-attention networks. Mỗi lớp tiếp theo nhận đầu vào từ lớp trước, cho phép mô hình xây dựng các tương tác bậc cao theo cách phân cấp. Các lớp này được kết nối bằng residual connections, tạo điều kiện cho việc huấn luyện sâu hơn và tránh vấn đề gradient vanishing. Cuối cùng, output từ tất cả các lớp được nối lại và đưa qua một fully connected layer để tạo ra dự đoán CTR cuối cùng.

## 3. Thành tựu đạt được

DESTINE được đánh giá trên hai bộ dữ liệu thực tế: tập dữ liệu quảng cáo trực tuyến của Alibaba và các bộ dữ liệu benchmark CTR công khai (bao gồm Avazu và Criteo). Kết quả thực nghiệm cho thấy DESTINE đạt được cải thiện nhất quán (consistent improvement) so với các baseline state-of-the-art:

- So với AutoInt (mô hình self-attention trước đây), DESTINE cải thiện AUC (Area Under Curve) đáng kể trên tất cả các bộ dữ liệu.
- Các baseline khác như DeepFM, xDeepFM cũng bị vượt qua về hiệu suất.
- Ablation studies (các thử nghiệm loại bỏ thành phần) chứng minh rằng cả tách biệt unary term lẫn pairwise interaction term đều góp phần quan trọng vào cải thiện hiệu suất.

Ngoài cải thiện hiệu suất dự đoán, paper còn chứng minh rằng DESTINE duy trì **tính hiệu quả tính toán** được cam kết, không tăng chi phí tính toán đáng kể so với các phương pháp tiền đó. Độ phức tạp tính toán và yêu cầu bộ nhớ vẫn ở mức hợp lý để triển khai thực tế trong các hệ thống quảng cáo lớn.

## 4. Hạn chế

Mặc dù DESTINE đạt được kết quả tốt, paper có một số hạn chế:

**Hạn chế tính toán:** Mặc dù được nhấn mạnh là hiệu quả, việc tách riêng unary và pairwise terms vẫn đòi hỏi tính toán thêm so với các phương pháp truyền thống. Kiến trúc multi-head attention cũng yêu cầu bộ nhớ không nhỏ.

**Giải thích interpretability:** Mặc dù tách biệt giúp học tốt hơn, không rõ liệu điều này có giúp model trở nên dễ diễn giải hơn hay không. Việc phân tích tấn công (adversarial analysis) hoặc robust của model không được thảo luận chi tiết.

**Mở rộng đến các loại dữ liệu khác:** Hầu hết các đánh giá tập trung vào dữ liệu quảng cáo thưa thớt. Hiệu quả của DESTINE trên các bộ dữ liệu khác hoặc loại tương tác feature khác chưa được khám phá.

**Hướng nghiên cứu tương lai:** Paper gợi ý các hướng phát triển tiếp theo như tích hợp các cơ chế chú ý tiên tiến hơn, khám phá các phương pháp kết hợp unary và pairwise terms một cách hiệu quả hơn, và mở rộng phương pháp đến các lĩnh vực ứng dụng khác ngoài CTR prediction.

---

## Tham khảo

- [DESTINE - ArXiv 2101.03654](https://arxiv.org/abs/2101.03654)
- [DESTINE - GitHub Repository](https://github.com/CRIPAC-DIG/DESTINE)
- [DESTINE - ResearchGate](https://www.researchgate.net/publication/348403056_Disentangled_Self-Attentive_Neural_Networks_for_Click-Through_Rate_Prediction)
