# Review Paper: A Universal Framework for Compressing Embeddings in CTR Prediction

**ArXiv ID:** [2502.15355](https://arxiv.org/abs/2502.15355)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết vấn đề quản lý bộ nhớ trong các hệ thống dự đoán CTR (Click-Through Rate) quy mô lớn. Bảng embedding có kích thước khổng lồ thường vượt quá giới hạn bộ nhớ GPU, buộc phải lưu trữ trên CPU và gây ra độ trễ đáng kể. Vấn đề này trở nên ngày càng cấp thiết khi các mô hình hiện đại cần xử lý hàng triệu hoặc tỷ feature trong các ứng dụng thực tế như quảng cáo và recommender systems.

Những phương pháp nén truyền thống thường mất đi thông tin quan trọng hoặc không tương thích với nhiều kiến trúc mô hình khác nhau. Cách tiếp cận model-agnostic được đề xuất cho phép áp dụng nén cho bất kỳ mô hình CTR nào mà không cần sửa đổi kiến trúc cốt lõi. Nghiên cứu này nhằm đạt được mục tiêu kép: giảm mạnh bộ nhớ (trên 50x) đồng thời duy trì hoặc cải thiện chất lượng dự đoán.

Động lực chính xuất phát từ nhu cầu thực tế về khả năng mở rộng: các bảng embedding có thể chứa 1 triệu đến hàng tỷ entries với chiều cao 40-128. Bài báo tập trung vào việc phát triển framework chung có thể integrate vào các hệ thống sản xuất hiện tại mà không cần redesign toàn bộ pipeline.

## 2. Phương pháp sử dụng

Framework MEC hoạt động theo hai giai đoạn được tách rời:

**Giai đoạn 1 - Huấn luyện:** Một mô hình CTR phụ trợ học các embedding ban đầu, sau đó chúng được encode và lượng tử hóa sử dụng Product Quantization (PQ). Codebook được lưu lại để sử dụng trong downstream tasks. PQ là kỹ thuật then chốt, phân tách mỗi embedding vector d-chiều thành M sub-vectors độc lập, mỗi cái được lượng tử hóa thành codeword gần nhất dựa trên khoảng cách Euclidean.

**Giai đoạn 2 - Inference:** Các feature đầu vào được transform thành quantized codes thông qua phương pháp được lưu, sau đó mapped thành compressed embeddings để huấn luyện và dự đoán. Điều này cho phép decoupling giữa compression learning và inference, cung cấp tính linh hoạt cao.

Hai thành phần chính là **Popularity-weighted Regularization (PWR)** và **Contrastive Learning**. PWR giải quyết vấn đề mất cân bằng trong phân bố mã codebook - các feature tần suất cao có xu hướng monopolize các codeword tốt, bỏ lại các feature hiếm gặp với biểu diễn kém. Phương pháp sử dụng transform logarithmic: r_j = ⌊log₂(n_j)⌋ để cân nhắc đóng góp của từng feature dựa trên tần suất.

Contrastive learning component tạo semi-synthetic negatives bằng cách random thay thế một index trong feature codes. Loss function được thiết kế để đạt được entropy đều giữa các mã và diversity cao giữa embeddings. Tổng hàm loss kết hợp: (1) reconstruction loss cho quantization accuracy, (2) regularization loss cho uniform code distribution, (3) binary classification loss cho CTR prediction task.

## 3. Thành tựu đạt được

Kết quả thực nghiệm trên ba datasets chính:
- **Criteo (45.8M interactions, 39 features):** Đạt 50x memory reduction, cải thiện AUC 0.4% so với GDCN baseline
- **Avazu (40.4M interactions, 22 features):** Memory reduction 50x, duy trì AUC hiệu suất cao
- **Industrial dataset (Huawei, 400M+ impressions):** Scaling lên 99.7x compression tuy nhiên với tradeoff nhỏ về accuracy

Embedding lookup time giảm khoảng 50% so với mô hình uncompressed. Mô hình duy trì hoặc cải thiện AUC trên tất cả datasets khi so sánh với baselines uncompressed. Codebook sizes ({256, 512, 1024, 2048}) và PQ layers ({2, 4, 8}) được tune tối ưu dựa trên độ phức tạp của từng feature set.

Framework đã được chấp nhận tại DASFAA 2025 và code được public trên GitHub, cho phép reproducibility cao trong cộng đồng nghiên cứu.

## 4. Hạn chế

Phương pháp yêu cầu training stage riêng biệt để học quantization, điều này có thể tốn kém về thời gian và tài nguyên tính toán. Hiệu suất nén phụ thuộc mạnh vào phân bố tần suất các feature - các dataset có phân bố đều có thể không đạt compression ratio cao như expected.

Áp dụng contrastive learning có thể làm tăng độ phức tạp training process. Bài báo không chi tiết về cách xử lý dynamic features hoặc streaming scenarios nơi codebook cần update theo thời gian. Future work cần khám phá online quantization methods để adapt với evolving data distributions trong production systems.
