# Review Paper: EGIN: Light-weight End-to-End Graph Interest Network for CTR Prediction in E-commerce Search

**ArXiv ID:** [2406.17745](https://arxiv.org/abs/2406.17745)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo nhận thấy CTR trong **e-commerce search khác biệt** so với recommendation: query là yếu tố quan trọng nhưng bị bỏ qua. Các mô hình graph hiện tại chủ yếu focus vào recommendation, dựa nhiều vào thông tin sequential item mà bỏ qua **query signals và query-item relationships**. Trong search, user intent được thể hiện qua query — model cần capture mối quan hệ giữa queries và items để hiểu search intent chính xác.

## 2. Phương pháp sử dụng

**EGIN** xây dựng 4 thành phần:

- **Query-item Heterogeneous Graph**: Biểu diễn cả queries và items trong cùng graph, capture **correlation và sequential information** giữa chúng
- **Light-weight Graph Sampling**: Giảm chi phí tính toán graph operations trong khi duy trì effectiveness — cho phép scale
- **Multi-interest Network**: Sử dụng graph embeddings để mô hình hóa **đa dạng mối quan hệ** giữa queries và items
- **End-to-end Training**: Graph embedding learning chia sẻ input với CTR prediction task → seamless deployment, không cần pipeline riêng cho graph

## 3. Thành tựu đạt được

- Lấp đầy khoảng cách recommendation vs **search-specific CTR**
- Chi phí training tương đối thấp nhờ light-weight sampling
- Hiệu quả trên cả **public và industrial datasets**
- End-to-end design cho deployment thuận tiện trong search systems

## 4. Hạn chế

- Thiếu con số AUC, LogLoss, CTR lift cụ thể trên public datasets
- "Chi phí thấp" nhưng không có con số cụ thể so sánh computation cost
- Chỉ test trên e-commerce search — generalization sang web search, video search chưa kiểm chứng
- Graph sampling algorithm complexity (time, space) không phân tích
