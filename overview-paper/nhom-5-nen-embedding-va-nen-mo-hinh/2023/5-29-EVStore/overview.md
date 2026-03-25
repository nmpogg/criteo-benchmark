# Review Paper: EVStore: Storage and Caching Capabilities for Scaling Embedding Tables in Deep Recommendation Systems

**DOI:** [ACM 10.1145/3575693.3575718](https://dl.acm.org/doi/10.1145/3575693.3575718)
**Năm:** 2023 | **Venue:** ASPLOS 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Deep Recommendation Systems (DRS) sử dụng embedding tables chứa **hàng tỷ vectors** yêu cầu hàng chục TB bộ nhớ. DRAM-heavy architectures tạo chi phí operational khổng lồ — gần **80% tất cả AI deployment costs tại Facebook (2020)** phục vụ DRS. Inference có tính "all-or-nothing": nếu bất kỳ EV table lookup nào chậm, toàn bộ request chậm. Các giải pháp hiện tại không khai thác structural regularity trong inference operations và không áp dụng domain-specific approximations. EVStore đề xuất hệ thống lưu trữ/caching 3 lớp giải quyết vấn đề này.

## 2. Phương pháp sử dụng

**Kiến trúc 3 lớp (3-layer EV table lookup):**

EVStore khai thác ba đặc tính của DRS inference:

1. **Locality exploitation**: Một số embeddings được truy cập thường xuyên hơn nhiều → ưu tiên cache các hot embeddings
2. **Structural regularity**: Tận dụng patterns đều đặn trong cách inference access embedding tables — các request có cấu trúc lặp lại
3. **Domain-specific approximations**: Sử dụng kỹ thuật xấp xỉ đặc thù miền (similar embeddings → approximate lookup) để giảm memory footprint

**Caching strategy** phân tích access patterns và tối ưu multi-tier caching cho hot/warm/cold embeddings.

## 3. Thành tựu đạt được

- **Giảm latency**: average **-23%**, p90 **-27%**
- **Tăng throughput**: **4x** so với baseline
- **Giảm memory**: **94%** reduction (chỉ cần 6% data trong memory) với chỉ **0.2% accuracy drop**
- Tác động kinh tế đáng kể cho các công ty triển khai DRS quy mô lớn (Facebook-scale)
- Chấp nhận tại **ASPLOS 2023** — hội thảo hàng đầu về kiến trúc hệ thống

## 4. Hạn chế

- **0.2% accuracy drop** cho 94% memory reduction — một số ứng dụng sensitive có thể không chấp nhận được
- Hiệu quả phụ thuộc vào **structural regularity** trong access patterns — workload không có tính quy luật sẽ kém hơn
- Hệ thống 3 lớp phức tạp triển khai, yêu cầu tối ưu cẩn thận cho từng deployment cụ thể
- Overhead quản lý complex caching strategy cần được cân nhắc
- Chưa chứng minh generalization sang tất cả DRS variants (cross-device vs on-device)
