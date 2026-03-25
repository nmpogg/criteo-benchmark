# Review Paper: Thorough Performance Benchmarking on Lightweight Embedding-based Recommender Systems

**ArXiv ID:** [2406.17335](https://arxiv.org/abs/2406.17335)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Các nghiên cứu về Lightweight Embedding-based Recommender Systems (LERSs) sử dụng **evaluation protocols không nhất quán** — mỗi paper tự chọn baselines, metrics, và settings riêng, khiến khó so sánh công bằng. Embedding tables chiếm phần lớn bộ nhớ trong recommendation models, nhưng chưa ai đánh giá hệ thống xem các phương pháp LERS nào thực sự hiệu quả.

**Motivation:** Cung cấp benchmarking toàn diện đánh giá performance, efficiency, và transferability của các LERS dưới cùng chuẩn đánh giá — bao gồm cả triển khai thực tế trên thiết bị edge.

## 2. Phương pháp sử dụng

**Comprehensive Evaluation Framework:**

1. **Multi-dimensional Assessment:**
   - **Performance:** AUC, Recall metrics
   - **Efficiency:** Latency, memory consumption
   - **Transferability:** Cross-task performance

2. **Multi-task Testing:**
   - Collaborative Filtering task
   - Content-based Recommendation task

3. **Edge Device Deployment:** Thử nghiệm trên **Raspberry Pi 4** — mô phỏng triển khai thực tế trên thiết bị edge

4. **Magnitude Pruning Baseline:** Phát triển simple magnitude pruning baseline để so sánh — đơn giản nhưng bất ngờ hiệu quả

5. **Standardized Protocols:** Quy trình đánh giá chuẩn hóa đảm bảo fair comparison

## 3. Thành tựu đạt được

- **Key finding:** Simple magnitude pruning **vượt trội** nhiều phương pháp LERS phức tạp — đặt câu hỏi về giá trị của complexity
- **Edge bottlenecks:** Xác định nút thắt hiệu suất cụ thể trong edge deployment
- **Task-dependent:** LERSs có hiệu suất khác biệt rõ rệt giữa collaborative filtering và content-based — không có one-size-fits-all
- **Open-source:** Framework đánh giá + code công khai cho community
- **Practical guidelines:** Tầm quan trọng của lựa chọn model theo context cụ thể

## 4. Hạn chế

- **Limited tasks:** Chỉ 2 recommendation tasks (collaborative filtering, content-based) — chưa bao quát CTR prediction, ranking
- **Basic baseline:** Magnitude pruning dù hiệu quả nhưng chưa so sánh với advanced structured pruning methods
- **Single edge device:** Chỉ test Raspberry Pi 4, chưa đánh giá mobile/IoT devices khác
- **Root cause analysis:** Không phân tích chi tiết nguyên nhân sự khác biệt hiệu suất giữa các LERS
- **Transferability clarity:** Cơ chế chuyển giao giữa tasks và datasets chưa được giải thích rõ ràng
