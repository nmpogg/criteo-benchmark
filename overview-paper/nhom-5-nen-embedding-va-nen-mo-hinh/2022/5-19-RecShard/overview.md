# Review Paper: RecShard: Statistical Feature-Based Memory Optimization for Industry-Scale Neural Recommendation

**ArXiv ID:** [2201.10095](https://arxiv.org/abs/2201.10095)
**Năm:** 2022
**Tác giả:** Meta AI
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding tables chiếm 99% không gian bộ nhớ trong DLRM nhưng có access patterns rất không đều và tỷ lệ sử dụng thấp (birthday paradox phenomenon). Hệ thống bộ nhớ nhiều tầng (GPU SRAM → GPU HBM → CPU DRAM → SSD) cần sharding strategy thông minh để tối ưu throughput.

**Motivation:** Phân bổ embedding tables hiện tại không xem xét đặc tính truy cập thực tế → nhiều hot embeddings nằm trên slow memory, cold embeddings chiếm chỗ trên fast memory. Cần **statistical feature-based sharding** để đặt đúng dữ liệu vào đúng tầng bộ nhớ.

## 2. Phương pháp sử dụng

**Fine-grained Embedding Table Partitioning dựa trên phân tích thống kê:**
- **Statistical Feature Analysis:** Phân tích phân bố training data để hiểu access patterns của từng embedding table
- **Birthday Paradox Modeling:** Mô hình hóa hash table underutilization — nhiều entries không bao giờ được truy cập
- **Tiered Memory Aware Sharding:** Tính toán bandwidth characteristics của từng tầng bộ nhớ, xác định vị trí tối ưu cho từng shard
- **Dynamic Placement:** Đặt hot shards vào fast memory (GPU HBM), cold shards vào slow memory (CPU DRAM/SSD)

## 3. Thành tựu đạt được

| Metric | Kết quả |
|--------|---------|
| **Training throughput** | 6× cải thiện so với baseline |
| **Load balance** | 12× cải thiện (giảm underutilization) |
| **Slow memory access** | Giảm 87× (ít truy cập vào bộ nhớ chậm) |

- Triển khai trên production-scale models tại Meta
- Không cần thay đổi kiến trúc model, áp dụng ngay trên hệ thống hiện tại

## 4. Hạn chế

- **Offline analysis:** Phương pháp dựa trên phân tích thống kê offline → không tối ưu nếu access patterns thay đổi theo thời gian
- **Hardware-specific:** Chiến lược sharding tối ưu cho một kiến trúc bộ nhớ cụ thể có thể không transfer tốt sang kiến trúc khác
- **Chưa thảo luận kịch bản kém:** Không phân tích khi nào phương pháp kém hiệu quả (e.g., uniform access patterns)
- **Complexity:** Yêu cầu hiểu biết sâu về memory bandwidth characteristics và hệ thống bộ nhớ nhiều tầng
- **Scalability chưa rõ:** Không đề cập scalability cho hệ thống cực lớn (petabyte-scale)
