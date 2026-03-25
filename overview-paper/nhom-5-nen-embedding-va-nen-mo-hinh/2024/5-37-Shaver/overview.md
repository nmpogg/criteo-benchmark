# Review Paper: Shaver: Single-shot Pruning for Recommendation Models via Shapley Values

**ArXiv ID:** [2411.13052](https://arxiv.org/abs/2411.13052)
**Năm:** 2024 | **Venue:** WWW 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Triển khai recommendation models trên thiết bị hạn chế tài nguyên (on-device) yêu cầu nén embedding tables. Các phương pháp pruning truyền thống cần **retraining cho mỗi budget constraint** — rất tốn kém. Paper đề xuất Shaver — phương pháp **single-shot pruning** không cần retraining, sử dụng lý thuyết trò chơi hợp tác (Cooperative Game Theory) để định lượng đóng góp của từng tham số.

**Motivation:** Dùng **Shapley values** — metric công bằng từ game theory — để đo lường chính xác đóng góp của mỗi embedding parameter, từ đó pruning thông minh chỉ trong một lần.

## 2. Phương pháp sử dụng

**Shapley Value-guided Embedding Reduction (Shaver):**

1. **Shapley Value Computation:**
   - Tính Shapley values để đo đóng góp của mỗi tham số embedding đến model performance
   - **Efficient estimation:** Phương pháp ước tính unbiased, giảm overhead đáng kể so với tính toán exact

2. **Single-shot Pruning:**
   - Rank parameters theo Shapley values
   - Remove parameters có đóng góp thấp nhất theo budget constraint
   - Một lần duy nhất — không cần iterative retraining

3. **Field-aware Codebook:**
   - Thay vì zero-out (loại bỏ hoàn toàn), sử dụng codebook theo field để **giữ lại thông tin**
   - Giảm thiểu information loss so với naive pruning

## 3. Thành tựu đạt được

- **Competitive performance** trên nhiều parameter budget levels
- **No retraining needed:** Single-shot approach tiết kiệm đáng kể chi phí tính toán
- **3 real-world datasets:** Kết quả tích cực trên cả 3
- **Practical scenarios:** Áp dụng thành công trong federated learning và streaming settings
- **Venue:** Accepted at WWW 2025 (top-tier web conference)

## 4. Hạn chế

- **Shapley computation cost:** Dù đã optimize, chi phí ước tính Shapley values vẫn có thể cao cho embedding tables rất lớn
- **Codebook complexity:** Field-aware codebook thêm độ phức tạp implementation, cần optimize cho on-device inference
- **Independence assumption:** Giả định về independence của embedding parameters chưa được kiểm chứng hoàn toàn
- **Time comparison missing:** Không so sánh chi tiết thời gian thực tế vs phương pháp retraining truyền thống
- **Scalability:** Khả năng mở rộng với số lượng parameters cực lớn (billions) chưa rõ
