# Review Paper: Sparsity-Preserving Differentially Private Training of Large Embedding Models

**ArXiv ID:** [2311.08357](https://arxiv.org/abs/2311.08357)
**Năm:** 2023 | **Venue:** NeurIPS 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Khi áp dụng DP-SGD (Differentially Private SGD) vào embedding models lớn, cơ chế thêm noise **phá hủy gradient sparsity** — biến sparse gradients thành dense, loại bỏ lợi thế tính toán tự nhiên. Embedding models tự nhiên tạo sparse gradients vì mỗi mini-batch chỉ kích hoạt một phần nhỏ embedding rows. Sparsity này giảm memory và communication overhead đáng kể. Tuy nhiên, DP mechanisms thêm noise vào tất cả dimensions, làm dense hóa gradients và tạo xung đột cơ bản giữa **privacy guarantees** và **training efficiency**. Bài báo đề xuất thuật toán duy trì cả hai.

## 2. Phương pháp sử dụng

**Hai thuật toán chính:**

1. **DP-FEST (Filtering-Enabled Sparse Training)**: Chỉ thêm noise vào gradients của các embedding rows được chọn trước (frequent rows), bảo tồn sparsity pattern. Thay vì noise toàn bộ, chỉ tập trung vào phần quan trọng nhất.

2. **DP-AdaFEST (Adaptive variant)**: Sử dụng thông tin mini-batch để **lựa chọn động** (adaptive) những buckets thông tin nhất. Áp dụng thresholding loại bỏ gradient entries không đáng kể — chỉ giữ entries mà đủ nhiều examples trong mini-batch đóng góp.

3. **DP-AdaFEST+**: Kết hợp DP-AdaFEST + DP-FEST, tạo hiệu suất còn tốt hơn.

## 3. Thành tựu đạt được

- **Giảm gradient computation**: DP-FEST ~10⁵x, DP-AdaFEST >5×10⁵x, DP-AdaFEST+ >**10⁶x** trên Criteo-Kaggle
- **Accuracy loss**: AUC loss dưới **0.005** — mức loss không đáng kể
- Duy trì comparable accuracy với baselines không có privacy protection
- Chấp nhận tại **NeurIPS 2023** — hội nghị ML hàng đầu thế giới
- Lần đầu tiên giải quyết xung đột DP vs sparsity cho embedding models

## 4. Hạn chế

- Chỉ Criteo-Kaggle được nêu chi tiết, generalization sang embedding models khác chưa kiểm chứng đầy đủ
- Ảnh hưởng cụ thể của epsilon (ε) và delta (δ) parameters trên privacy-utility tradeoff không được phân tích kỹ
- Scalability cho embedding vocabularies cực lớn không được thảo luận
- Giả định sparsity patterns tồn tại — nếu models trở nên dense, hiệu quả giảm
- Không có convergence guarantees formal dưới sparsity constraints
- Ứng dụng cụ thể cho embedding models, mở rộng sang deep learning tổng quát chưa rõ
