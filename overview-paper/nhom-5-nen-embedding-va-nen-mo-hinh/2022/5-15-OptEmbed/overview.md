# Review Paper: OptEmbed: Learning Optimal Embedding Table for Click-Through Rate Prediction

**ArXiv ID:** [2208.04482](https://arxiv.org/abs/2208.04482)
**Năm:** 2022 | **Venue:** CIKM 2022
**Tác giả:** Fuyuan Lyu, Xing Tang, Hong Zhu, Huifeng Guo, Yingxue Zhang, Ruiming Tang, Xue Liu
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding tables trong CTR prediction là 2D tensors (feature values × embedding dimensions) chiếm lượng bộ nhớ rất lớn. Các phương pháp hiện tại dùng uniform embedding dimension cho tất cả fields — gây lãng phí cho fields đơn giản và thiếu capacity cho fields phức tạp. Pruning thưa tạo sparse tables khó deploy (cần custom kernels).

**Motivation:** Tìm **embedding dimension tối ưu riêng cho từng feature field**, tạo compact tables dễ deploy trên production mà vẫn giữ hoặc cải thiện accuracy.

## 2. Phương pháp sử dụng

Framework gồm 3 thành phần chính:

1. **Learnable Pruning:** Loại bỏ embedding dimensions dư thừa bằng trainable thresholds dựa trên feature importance — tự động xác định field nào cần bao nhiêu dimensions
2. **Uniform Sampling Scheme:** Train tất cả candidate architectures trong supernet đồng đều, cho phép đồng thời tối ưu architecture parameters và pruning thresholds
3. **Evolution Search:** Dùng evolutionary algorithms tìm tổ hợp embedding dimensions tối ưu cho từng field trong khoảng parameter budget cho phép

## 3. Thành tựu đạt được

- **Kích thước model:** Giảm đáng kể so với baseline (uniform dimensions)
- **Accuracy:** Thậm chí **cải thiện performance** trên public CTR datasets — compact table loại bỏ noise từ dimensions dư thừa
- **Generalizability:** Framework-agnostic, hoạt động với nhiều loại CTR models khác nhau (DeepFM, Wide&Deep, etc.)
- **Practical:** Tạo dense compact tables dễ deploy, không cần custom sparse kernels

## 4. Hạn chế

- **Search cost:** Chi phí computational của evolution search process không được công bố chi tiết
- **Scalability chưa rõ:** Chưa kiểm chứng trên massive feature sets (100M+ features)
- **Deployment overhead:** Chi phí trong giai đoạn architecture search chưa được phân tích
- **Limited validation:** Chủ yếu test trên public datasets, chưa validate trên production-scale systems
