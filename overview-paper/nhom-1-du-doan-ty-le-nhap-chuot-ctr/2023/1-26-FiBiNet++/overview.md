# Overview: FiBiNet++: Reducing Model Size by Low Rank Feature Interaction Layer for CTR Prediction

**ArXiv ID:** [2209.05016](https://arxiv.org/abs/2209.05016)
**Venue:** CIKM 2023
**Năm:** 2023
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

- FiBiNet gốc đạt hiệu suất cao nhưng kích thước quá lớn (hàng triệu tham số), hạn chế triển khai trong môi trường production
- Lấy cảm hứng từ LoRA trong NLP: giả thuyết feature interactions trong CTR có "chiều nội tại thấp" (low intrinsic dimension)
- Mục tiêu cụ thể: giảm 12–16x tham số non-embedding trong khi duy trì hoặc cải thiện hiệu suất
- Chi phí lưu trữ, tốc độ suy luận, và năng lượng là bottleneck thực tế cho quảng cáo/recommendation quy mô lớn
- Chưa có công trình nào áp dụng low-rank decomposition một cách hệ thống vào bilinear feature interaction layers cho CTR

## 2. Phương pháp sử dụng

- **Low Rank Decomposition:** Ma trận tương tác W = U × V^T, với U ∈ R^(m×r), V ∈ R^(n×r), r << min(m,n)
- Áp dụng vào Bi-linear+ Module của FiBiNet: giảm params từ m×n xuống r×(m+n) (factor 2)
- Tính toán hiệu quả: U·(V^T·x) thay vì W·x → giảm từ O(m×n) xuống O(r×(m+n))
- Giữ nguyên kiến trúc FiBiNet tổng thể (embedding, feature importance via SENET, bilinear interaction) — chỉ thay interaction layer
- Hàm kích hoạt tuyến tính cho lớp low-rank để duy trì expressiveness
- Rank r là hyperparameter, thường 4–8 cho cân bằng tối ưu giữa performance và compression
- SGD/Adam optimizer, BCE loss, L2 regularization trên U và V để tránh overfitting

## 3. Thành tựu đạt được

- Giảm tham số non-embedding: 12.7x, 12.9x, 16x lần lượt trên 3 datasets
- Vượt trội tất cả SOTA bao gồm FiBiNet gốc dù ít params hơn — nghịch lý tích cực (regularization effect)
- Training efficiency tăng: 58.76%, 62.30%, 39.39% tương ứng trên 3 datasets
- Inference speed tăng: 41.66%, 81.03%, 37.50% tương ứng
- Datasets: 3 public (bao gồm Avazu), baselines: DNN, Wide&Deep, DeepFM, FiBiNet gốc
- Chấp nhận tại CIKM 2023

## 4. Hạn chế

- Hiệu suất phụ thuộc mạnh vào rank r — quá nhỏ → underfitting; quá lớn → không đạt mục tiêu nén
- Giả thuyết "low intrinsic dimension" của feature interactions là heuristic, chưa có chứng minh lý thuyết
- Chỉ so sánh chủ yếu với FiBiNet gốc và DNN — thiếu comparison với các low-rank/knowledge distillation approaches khác
- Chưa kiểm tra hiệu quả riêng biệt trên categorical vs numerical features
- Chỉ 3 public datasets, chưa test production-scale với hàng tỷ samples
