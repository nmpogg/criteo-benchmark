# Review Paper: EST — Towards Efficient Scaling Laws in Click-Through Rate Prediction via Unified Modeling

**ArXiv:** [2602.10811](https://arxiv.org/abs/2602.10811) | **Năm:** 2026
**Tác giả:** Mingyang Liu, Yong Bai, Zhangming Chan, Sishuo Chen, Xiang-Rong Sheng, Han Zhu, Jian Xu, Xinyang Chen

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **scaling hiệu quả các mô hình CTR prediction** trong môi trường công nghiệp, lấy cảm hứng từ scaling laws đã thành công trong NLP (GPT) và CV:

- **Vấn đề mất tín hiệu do early aggregation:** Các phương pháp CTR hiện tại thực hiện aggregation sớm trên user behaviors (ví dụ: pooling toàn bộ click history thành 1 vector), làm mất fine-grained signals. Một user click 100 items khác nhau bị nén thành 1 vector duy nhất → mất thông tin chi tiết về từng hành vi.
- **Thiếu scaling laws ổn định:** Trong NLP, tăng model size → hiệu suất tăng theo power-law dự đoán được. Trong CTR, tăng model size không đảm bảo cải thiện tương ứng — đôi khi performance đi ngang hoặc giảm.

**Mục tiêu:** Xây dựng kiến trúc CTR cho phép scaling ổn định theo power-law, tương tự như các large language models.

## 2. Phương pháp sử dụng

**EST (Efficiently Scalable Transformer)** — xử lý toàn bộ raw inputs như unified sequence:

**1. Unified Sequence Modeling:**
- Thay vì aggregate behaviors sớm, EST giữ nguyên tất cả raw inputs (user features, item features, behavior sequences) dưới dạng **một chuỗi thống nhất**
- Bảo toàn fine-grained information ở mọi cấp độ

**2. Lightweight Cross-Attention (LCA):**
- Loại bỏ **self-interactions dư thừa** — trong full self-attention, mỗi behavior attend vào mọi behavior khác, phần lớn là noise
- LCA chỉ giữ lại cross-feature dependencies quan trọng (giữa user features và item features, giữa behaviors và target item)
- Giảm complexity từ O(n²) xuống mức thấp hơn đáng kể

**3. Content Sparse Attention (CSA):**
- Sử dụng **content similarity** để dynamically xác định behaviors nào có giá trị cao nhất
- Thay vì attend đều lên toàn bộ sequence, CSA ưu tiên behaviors có nội dung tương tự target item
- User search "laptop" → CSA tự động ưu tiên lịch sử click liên quan electronics, bỏ qua lịch sử click food

**Kết hợp:** LCA + CSA cho phép EST scale lên model lớn mà vẫn giữ computational cost hợp lý.

## 3. Thành tựu đạt được

- **Thiết lập stable power-law scaling** cho CTR prediction — lần đầu tiên chứng minh CTR models có thể scale như language models
- **Triển khai production trên Taobao display advertising:**
  - **+3.27% RPM** (Revenue Per Mille) — doanh thu trên 1000 lần hiển thị
  - **+1.22% CTR lift** — tỷ lệ click tăng
  - Đây là metrics rất đáng kể trong industrial setting (thường improvement ~0.1-0.5% đã có giá trị lớn)
- **Predictable scaling:** Có thể dự đoán performance khi tăng model size, giúp quyết định đầu tư tài nguyên hiệu quả
- **Practical framework:** Cung cấp hướng dẫn thực tế cho scaling industrial CTR models

## 4. Hạn chế

- **Đánh giá chủ yếu trên Taobao:** Generalization sang các platforms/domains khác chưa được xác minh
- **Computational cost vẫn cao:** Multi-head attention dù đã tối ưu (LCA, CSA) vẫn tốn tài nguyên hơn đáng kể so với simple MLP-based CTR models
- **Extreme long sequences:** Chưa rõ hiệu suất khi sequence length rất lớn (>10K behaviors) — LCA/CSA có thể gặp bottleneck
- **Unified sequence assumption:** Giả định mọi features có thể biểu diễn trong cùng sequence space có thể không phù hợp với mọi loại dữ liệu
