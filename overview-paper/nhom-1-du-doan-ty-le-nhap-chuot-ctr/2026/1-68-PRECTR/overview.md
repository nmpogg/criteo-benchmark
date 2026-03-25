# Review Paper: PRECTR — A Synergistic Framework for Integrating Personalized Search Relevance Matching and CTR Prediction

**ArXiv:** [2503.18395](https://arxiv.org/abs/2503.18395) | **Năm:** 2026
**Tác giả:** Rong Chen, Shuzhi Cao, Ailong He, Shuguang Han, Jufeng Chen

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **kết hợp search relevance matching và CTR prediction** — hai chức năng cốt lõi trong hệ thống tìm kiếm/đề xuất mà truyền thống được xử lý riêng rẽ:

- **Vấn đề pipeline tách rời:** Hệ thống search truyền thống dùng 2 model riêng biệt: (1) relevance model đánh giá mức độ liên quan query-item, (2) CTR model dự đoán xác suất click. Hai model hoạt động độc lập rồi kết hợp kết quả để ranking. Sự tách biệt này gây inconsistency — relevance model cho item A điểm cao nhưng CTR model lại ưu tiên item B.
- **Relevance thiếu personalization:** Relevance models truyền thống chỉ dựa trên objective text matching (query "điện thoại" → so khớp với title sản phẩm), hoàn toàn bỏ qua sở thích cá nhân. Hai users cùng search "điện thoại" nhưng một người thích Samsung, người kia thích iPhone — relevance model trả kết quả giống nhau.

**Ý tưởng chính:** Thống nhất relevance + CTR vào một framework duy nhất, đồng thời bổ sung personalization vào relevance scoring.

## 2. Phương pháp sử dụng

**PRECTR Framework** gồm 4 thành phần chính:

**1. Unified Relevance-CTR Integration:**
- Tích hợp CTR prediction và relevance matching vào **cùng một model**, loại bỏ pipeline tách rời
- Sử dụng **conditional probability fusion mechanism** — CTR được tính có điều kiện trên relevance: P(click) = P(click|relevant) × P(relevant)
- Đảm bảo items có CTR cao nhưng irrelevant không bị đề xuất

**2. Personalized Relevance Enhancement:**
- Phân tích **past preferences của similar users** cho cùng query
- Khi user search "laptop", hệ thống xem users tương tự đã click gì → customize relevance score cho từng user
- Chuyển relevance từ objective (text matching) sang subjective (user-aware)

**3. Two-Stage Training Strategy:**
- Stage 1: Pretrain relevance component
- Stage 2: Joint fine-tune cả relevance + CTR
- Tránh convergence issues khi train hai tasks đồng thời từ đầu

**4. Semantic Consistency Regularization:**
- Regularization đặc biệt ngăn mô hình promote items có high CTR nhưng low relevance
- Đảm bảo semantic consistency: items được đề xuất phải vừa relevant vừa likely to be clicked

## 3. Thành tựu đạt được

- **Unified modeling vượt trội** so với paradigm divide-and-conquer truyền thống (tách riêng relevance và CTR)
- **Online A/B testing thành công** trên production system — chứng minh practical effectiveness, không chỉ offline
- **Kết quả trên production datasets** — thử nghiệm trên hệ thống thực tế phục vụ users thật
- **Framework tổng quát:** Conditional probability fusion có thể áp dụng cho bất kỳ cặp tasks nào cần kết hợp trong ranking

## 4. Hạn chế

- **Chỉ đánh giá trên proprietary datasets:** Không có kết quả trên public benchmarks (Criteo, Avazu, etc.), khó so sánh công bằng với các phương pháp khác
- **Thiếu improvement percentages cụ thể** trong abstract — "effectiveness and superiority" nhưng không có con số
- **Two-stage training phức tạp hơn** end-to-end training đơn giản
- **Phụ thuộc vào similar user identification:** Chất lượng personalized relevance phụ thuộc vào khả năng tìm đúng nhóm users tương tự
- **Generalization chưa rõ:** Kết quả chỉ trên production datasets của một hệ thống cụ thể
