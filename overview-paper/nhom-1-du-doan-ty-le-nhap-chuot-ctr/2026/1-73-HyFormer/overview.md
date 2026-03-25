# Review Paper: HyFormer — Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction

**ArXiv:** [2601.12681](https://arxiv.org/abs/2601.12681) | **Năm:** 2026
**Tác giả:** Yunwen Huang, Shiyong Hong, Xijun Xiao, Jinqiu Jin, Xuanyuan Luo, Zhe Wang, Zheng Chai, Shikang Wu, Yuchao Zheng, Jingjian Lin

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **xử lý đồng thời sequence modeling và feature interaction** trong CTR prediction tại quy mô công nghiệp, phân tích lại vai trò của từng thành phần:

- **Decoupled pipeline hiện tại:** Hệ thống CTR truyền thống xử lý tuần tự: (1) sequence model trích xuất user interest từ behavior history → output vector, (2) feature interaction model kết hợp output đó với các features khác. Hai bước tách rời → mất cơ hội tối ưu đồng thời.
- **Trade-off giữa sequence length và computation:** User behavior sequences trong production có thể dài hàng nghìn items. Full attention (O(n²)) không khả thi. Nhưng truncation (cắt bớt) mất thông tin. Cần kiến trúc xử lý long sequences hiệu quả.
- **Non-sequential features bị bỏ rơi:** Trong decoupled pipeline, non-sequential features (user demographics, item attributes, context) chỉ được dùng ở giai đoạn feature interaction — không tham gia vào sequence modeling, mất cơ hội guide extraction.

**Ý tưởng chính:** Thống nhất sequence modeling + feature interaction vào **single hybrid transformer backbone**, thay vì pipeline tách rời.

## 2. Phương pháp sử dụng

**HyFormer (Hybrid Transformer)** — 2 cơ chế xen kẽ qua nhiều layers:

**1. Query Decoding:**
- Mở rộng non-sequential features thành **Global Tokens** — biến user demographics, item attributes thành tokens có thể attend
- Decode long behavior sequences bằng **key-value representations** cached qua layers
- Global Tokens đóng vai trò queries → attend vào behavior key-values → trích xuất relevant information
- Mỗi layer refine thêm: layer đầu capture general patterns, layers sau capture fine-grained interests

**2. Query Boosting:**
- Tăng cường **cross-query interactions** (giữa các Global Tokens) và **cross-sequence interactions** (giữa sequence và non-sequence)
- Sử dụng **efficient token mixing** thay vì full attention — giảm cost
- Cho phép non-sequential features guide sequence modeling và ngược lại

**Iterative refinement:** Hai cơ chế xen kẽ qua N layers, mỗi layer tinh chỉnh semantic representations thêm. Layer 1 cho rough understanding, layer N cho fine-grained prediction.

## 3. Thành tựu đạt được

- **Vượt trội LONGER và RankMixer** — hai baselines mạnh gần đây — với **cùng computational budget**
- **Scaling performance tốt:** Tăng parameters và FLOPs → improvement ổn định, không bão hòa
- **A/B testing trong production:** Hệ thống high-traffic, đạt **"significant gains over deployed SOTA models"**
- **Billion-scale validation:** Kiểm chứng trên industrial datasets quy mô tỷ records
- **Unified architecture:** Đơn giản hóa pipeline từ 2-stage sang single backbone

## 4. Hạn chế

- **Thiếu specific metrics:** Không báo cáo AUC improvement, CTR lift, hay revenue gains cụ thể
- **Maintenance complexity:** Hybrid architecture (decoding + boosting xen kẽ) phức tạp hơn simple pipeline, khó debug khi gặp vấn đề
- **Training cost:** Iterative refinement qua nhiều layers tăng training time
- **Memory cho KV cache:** Cached key-value representations qua layers chiếm memory đáng kể
- **Chưa so sánh latency:** Không rõ inference speed so với decoupled pipeline truyền thống
