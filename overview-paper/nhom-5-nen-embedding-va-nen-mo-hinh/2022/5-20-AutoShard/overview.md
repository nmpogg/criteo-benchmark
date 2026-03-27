# Review Paper: AutoShard: Automated Embedding Table Sharding for Recommender Systems

**ArXiv ID:** [2208.06399](https://arxiv.org/abs/2208.06399)
**Năm:** 2022 | **Venue:** KDD 2022
**Tác giả:** Meta AI
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Phân phối hàng trăm embedding tables qua nhiều devices trong hệ thống recommendation là bài toán **NP-hard**. Manual sharding và heuristic-based strategies không scale khi số lượng tables và devices tăng lên. Cần cân bằng cả computational cost và storage cost qua các devices.

**Motivation:** Tự động hóa quy trình sharding với khả năng **học từ các tác vụ trước** và generalize cho scenarios mới mà không cần fine-tuning — giải quyết NP-hard problem bằng learned approach.

## 2. Phương pháp sử dụng

Kết hợp **Neural Cost Model + Deep Reinforcement Learning (DRL):**

1. **Neural Cost Model:** Mạng nơ-ron dự đoán multi-table costs trên các devices khác nhau
   - Input: Embedding table characteristics (size, access frequency), device specifications
   - Output: Predicted cost distribution (latency + memory)

2. **DRL Solver:** Học policy để giải NP-hard partition problem
   - State: Cấu hình sharding hiện tại
   - Action: Assign table → device
   - Reward: Minimize total cost (latency + memory)

3. **Transfer Learning:** Policies đã học **generalize** sang:
   - Số lượng tables khác nhau
   - Unseen data ratios
   - Mà không cần fine-tuning

## 3. Thành tựu đạt được

- **Vượt heuristics:** Tốt hơn greedy và rule-based approaches
- **Tốc độ:** Shard hàng trăm tables trong **vài giây**
- **Transferability:** Policy học từ synthetic data → transfer tốt sang production data
- **Production deployment:** Deployed thành công tại Meta production environment
- **Venue:** Accepted to KDD 2022 (top-tier conference)

## 4. Hạn chế

- **Black box:** DRL policy khó giải thích tại sao đưa ra quyết định cụ thể → khó debug khi kết quả không tốt
- **Training cost:** Phải huấn luyện neural cost model + DRL agent trước khi sử dụng
- **Cost model accuracy:** Hiệu quả phụ thuộc vào accuracy của neural cost model — sai cost model → sai sharding
- **Limited baselines:** Không so sánh chi tiết với advanced heuristics ngoài greedy
- **Extreme cases:** Chưa rõ performance khi configuration quá khác biệt so với training data
