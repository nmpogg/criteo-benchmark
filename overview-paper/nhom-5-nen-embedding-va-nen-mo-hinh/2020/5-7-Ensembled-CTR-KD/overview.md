# Review Paper: Ensembled CTR Prediction via Knowledge Distillation

**ArXiv ID:** [2011.04106](https://arxiv.org/abs/2011.04106)
**Năm:** 2020
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Nghiên cứu gần đây đã tập trung vào việc xây dựng các kiến trúc mạng phức tạp hơn để nắm bắt tốt hơn các tương tác tính năng phức tạp và hành vi người dùng động trong các mô hình dự đoán Click-Through Rate (CTR). Tuy nhiên, độ phức tạp gia tăng này gây ra một vấn đề quan trọng: nó làm chậm đáng kể quá trình inference trực tuyến và cảnh báo việc áp dụng các mô hình này trong các ứng dụng thực tế yêu cầu độ trễ thấp.

Bài báo đề xuất một chiến lược huấn luyện mới dựa trên Knowledge Distillation (KD), thay vì tiếp tục xây dựng các kiến trúc mô hình phức tạp hơn. Ý tưởng cốt lõi là: thay vì sử dụng một mô hình phức tạp lớn trong production, hãy sử dụng một mô hình học sinh đơn giản nhưng được huấn luyện bằng kiến thức từ một hoặc nhiều mô hình thầy giáo phức tạp.

## 2. Phương pháp sử dụng

Bài báo đề xuất một framework Knowledge Distillation dựa trên ensemble để dự đoán CTR. Phương pháp bao gồm các thành phần chính sau:

**Framework Teacher-Student:** Thay vì chỉ sử dụng một mô hình thầy, paper khám phá sử dụng một ensemble mạnh mẽ gồm nhiều mô hình thầy phức tạp để transfer kiến thức cho một mô hình học sinh vanilla DNN đơn giản. Cách tiếp cận ensemble này cho phép thu thập kiến thức từ nhiều quan điểm mô hình khác nhau.

**Teacher Gating:** Kỹ thuật mới được đề xuất để xác định và cân bằng đóng góp của các mô hình thầy khác nhau. Thay vì coi tất cả các thầy là bình đẳng, teacher gating học được cách kết hợp các dự đoán từ các thầy khác nhau một cách tối ưu.

**Early Stopping bằng Distillation Loss:** Một kỹ thuật mới để dừng quá trình huấn luyện dựa trên distillation loss thay vì chỉ dựa trên validation loss truyền thống. Điều này giúp tránh overfitting và cải thiện khả năng tổng quát hóa của mô hình.

## 3. Thành tựu đạt được

Bài báo tiến hành các thí nghiệm toàn diện so sánh với 12 mô hình baseline khác nhau trên ba bộ dữ liệu công nghiệp (industrial datasets). Kết quả khả nhi đạt được:

- Mô hình học sinh DNN đơn giản, được huấn luyện bằng KD từ ensemble thầy, đạt được độ chính xác dự đoán CAO HƠNSO VỚI CÁC MÔ HÌNH THẦY.
- Cải tiến AUC đáng kể so với các mô hình state-of-the-art hiện tại.
- Kết quả không chỉ được xác nhận trong offline testing mà còn được xác thực thông qua online A/B testing trong môi trường production thực tế.

Thành công của phương pháp được chứng minh bằng cả offline evaluation (trên các tập dữ liệu công nghiệp) và online A/B testing, cho thấy sự hữu dụng thực tế của framework.

## 4. Hạn chế

Mặc dù paper báo cáo kết quả tích cực, nhưng có một số hạn chế tiềm ẩn:

**Overhead tính toán trong huấn luyện:** Mặc dù mô hình học sinh là nhẹ, quá trình huấn luyện yêu cầu tính toán đầu ra từ nhiều mô hình thầy. Điều này làm tăng chi phí tính toán trong giai đoạn training, mặc dù inference sau đó là nhanh.

**Phụ thuộc vào chất lượng thầy:** Phương pháp distillation phụ thuộc mạnh vào chất lượng của các mô hình thầy. Nếu tất cả các thầy đều có bias hoặc hạn chế tương tự, học sinh có thể inherit những hạn chế đó. Paper không thảo luận chi tiết về cách chọn lựa các mô hình thầy khác nhau.

**Thiếu chi tiết về metrics cụ thể:** Paper báo cáo "cải tiến đáng kể" nhưng không cung cấp các con số AUC, liftage, hoặc các chỉ số hiệu suất khác trong tóm tắt, hạn chế khả năng so sánh định lượng. Thêm vào đó, tính tổng quát hóa của phương pháp đối với các kiến trúc thầy khác ngoài những cái được kiểm tra trong paper vẫn là câu hỏi mở.
