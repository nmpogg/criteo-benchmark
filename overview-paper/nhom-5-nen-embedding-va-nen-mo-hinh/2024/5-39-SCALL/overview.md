# Review Paper: SCALL: Scalable Dynamic Embedding Size Search for Streaming Recommendation

**ArXiv ID:** [2407.15411](https://arxiv.org/abs/2407.15411)
**Năm:** 2024 | **Venue:** CIKM 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Trong hệ thống khuyến nghị streaming, dân số users và items **liên tục tăng** → embedding tables phát triển vô hạn, vượt quá giới hạn bộ nhớ. Các phương pháp hiện tại giả sử kích thước embedding chỉ tăng cùng tần suất (monotonic), không thể điều chỉnh giảm khi entity trở nên ít active.

**Motivation:** Cần phương pháp **dynamic** có thể cả tăng lẫn giảm kích thước embedding theo tần suất hoạt động của user/item, đồng thời tuân thủ fixed memory budget trong môi trường streaming.

## 2. Phương pháp sử dụng

**SCALL — Scalable Dynamic Embedding Size Search:**

1. **Probabilistic Sampling:** Lấy mẫu xác suất các kích thước embedding từ phân phối xác suất với budget constraint — đảm bảo tổng memory không vượt quá giới hạn

2. **RL-based Search:** Reinforcement Learning agent học policy điều chỉnh kích thước embedding động:
   - Tăng dimensions cho entities active nhiều
   - Giảm dimensions cho entities ít active
   - Cân bằng tổng thể theo memory budget

3. **Fixed-length State Vectors:** Dùng mean pooling để duy trì state vectors cố định — independent với số lượng users/items thay đổi

4. **Unseen Entity Handling:** Khả năng gán kích thước embedding phù hợp cho users/items chưa từng thấy trước đó

## 3. Thành tựu đạt được

- **Dynamic adjustment:** Tăng/giảm embedding dimensions dựa trên tần suất — giải quyết monotonic limitation
- **Budget compliance:** Duy trì memory constraint trong suốt quá trình streaming
- **Scalability:** Mở rộng được đến datasets có kích thước thay đổi liên tục
- **2 public datasets:** Chứng minh hiệu quả vượt trội
- **Venue:** CIKM 2024, code công khai

## 4. Hạn chế

- **Extreme distributions:** Probabilistic sampling có thể không tối ưu cho phân phối tần suất cực kỳ skewed
- **RL convergence:** Thời gian hội tụ của RL-based search trên streaming data thực tế chưa rõ
- **Mean pooling overhead:** Chi phí computational của mean pooling chưa được phân tích chi tiết
- **Limited datasets:** Chỉ đánh giá trên 2 datasets — chưa test trên production-scale streaming systems
- **Extreme growth:** Chưa kiểm chứng khi tốc độ tăng trưởng user/item cực nhanh
