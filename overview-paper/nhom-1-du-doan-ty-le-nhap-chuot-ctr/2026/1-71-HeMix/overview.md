# Review Paper: HeMix — Query-Mixed Interest Extraction and Heterogeneous Interaction for Scalable CTR in Industrial Recommender Systems

**ArXiv:** [2602.09387](https://arxiv.org/abs/2602.09387) | **Năm:** 2026
**Tác giả:** Fangye Wang, Guowei Yang, Xiaojiang Zhou, Song Yang, Pengjie Wang

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **feature interaction learning cho CTR prediction trong hệ thống đề xuất công nghiệp**, tập trung vào hai thách thức đặc thù của production systems:

- **Sparse multi-field data:** Dữ liệu CTR trong thực tế rất thưa — đa số feature combinations chưa từng xuất hiện trong training data. Ví dụ: user mới + item mới + context mới → không có historical interaction nào.
- **Extremely long user behavior sequences:** Users tích lũy hàng nghìn đến hàng chục nghìn behaviors theo thời gian. Xử lý toàn bộ sequence với full attention có complexity O(n²) — không khả thi cho real-time serving.

**Mục tiêu:** Thiết kế mô hình vừa capture effective feature interactions, vừa xử lý được long sequences, vừa scale hiệu quả khi tăng model size.

## 2. Phương pháp sử dụng

**HeMix Model** gồm 2 thành phần chính:

**1. Query-Mixed Interest Extraction Module:**
- Capture user preferences qua **hai cơ chế song song**:
  - **Dynamic query:** Target-aware extraction — trích xuất interests liên quan đến candidate item cụ thể (user quan tâm gì khi nhìn thấy item X?)
  - **Fixed query:** Target-independent extraction — trích xuất general interests không phụ thuộc candidate (user nói chung thích gì?)
- Xử lý cả **historical behaviors** (long-term) và **immediate behaviors** (real-time session)
- "Query-Mixed" = kết hợp outputs từ dynamic + fixed queries để có representation toàn diện

**2. HeteroMixer Block:**
- **Thay thế hoàn toàn self-attention** bằng kiến trúc hiệu quả hơn gồm 3 pipelines:
  - **Multi-head Token Fusion:** Trộn thông tin giữa các tokens qua multiple heads (tương tự MLP-Mixer)
  - **Heterogeneous Interaction:** Tương tác giữa các loại features khác nhau (numerical × categorical, user × item)
  - **Group-aligned Reconstruction:** Tái cấu trúc representations theo nhóm features có liên quan
- Hiệu quả hơn self-attention: giảm complexity mà vẫn capture multi-granularity interactions

## 3. Thành tựu đạt được

- **Scaling efficiency đã chứng minh:** Tăng parameters → consistent accuracy improvements (không bão hòa sớm)
- **Triển khai production trên AMAP (AutoNavi/Amap — nền tảng maps/navigation lớn nhất Trung Quốc):**
  - **+3.61% GMV** (Gross Merchandise Volume) — giá trị hàng hóa giao dịch
  - **+2.78% PV_CTR** (Page View Click-Through Rate)
  - **+2.12% UV_CVR** (Unique Visitor Conversion Rate)
  - Đây là improvements rất lớn trong industrial setting — thường 0.1-1% đã có giá trị kinh doanh đáng kể
- **Outperform DLRM baseline** (DLRM là mô hình production phổ biến từ Meta) trên nhiều metrics

## 4. Hạn chế

- **Complexity cao:** HeteroMixer block với 3 pipelines (token fusion + heterogeneous interaction + group reconstruction) khó maintain và debug trong production
- **Trade-off latency chưa rõ:** Paper báo cáo accuracy gains nhưng chưa chi tiết inference latency so với baselines
- **Đánh giá chủ yếu trên AMAP:** Generalization sang các domains khác (e-commerce, news, video) chưa được xác minh
- **Memory constraints:** Long sequence processing vẫn bị giới hạn bởi GPU memory, dù HeteroMixer hiệu quả hơn self-attention
- **Hyperparameter tuning:** 3 pipelines trong HeteroMixer tạo ra nhiều hyperparameters cần tune
