# Review Paper: CERP: Learning Compact Compositional Embeddings via Regularized Pruning for Recommendation

**ArXiv ID:** [2309.03518](https://arxiv.org/abs/2309.03518)
**Năm:** 2023 | **Venue:** ICDM 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Trong recommendation systems, mỗi entity (user/item) được biểu diễn bằng embedding vector có dimensionality cố định (vd: 128). Với hàng triệu users/items, embedding table trở thành memory bottleneck lớn nhất. Các phương pháp nén hiện tại (hashing, sparsification) hy sinh accuracy đáng kể dưới ràng buộc bộ nhớ chặt. CERP giải quyết bài toán: làm sao nén embedding table mạnh mẽ mà vẫn giữ được accuracy, bằng cách kết hợp compositional embeddings với regularized pruning.

## 2. Phương pháp sử dụng

**CERP (Compositional Embedding with Regularized Pruning):**

- Thay vì dùng một embedding vector lớn, mỗi entity được biểu diễn bằng **cặp embeddings từ hai meta-embedding tables** nhỏ hơn đáng kể (independent)
- Hai meta-embedding tables được **jointly pruned** thông qua **learnable element-wise thresholds** — mỗi element tự học ngưỡng cắt tỉa riêng
- Cơ chế **regularized pruning** khuyến khích hai sparse tables lưu giữ thông tin **mutually complementary** (bổ sung nhau), giảm redundancy tối đa
- Framework **model-agnostic**: tương thích với các latent factor models hiện có mà không cần thay đổi kiến trúc

## 3. Thành tựu đạt được

- Chấp nhận tại **ICDM 2023** (hội thảo đẳng cấp cao về data mining)
- Vượt trội state-of-the-art baselines trên hai real-world datasets dưới nhiều memory budgets khác nhau
- Model-agnostic: dễ tích hợp vào existing recommendation models
- Code công khai: [github.com/xurong-liang/CERP](https://github.com/xurong-liang/CERP)
- Cơ chế complementary giữa hai tables giúp giảm information loss so với single-table pruning

## 4. Hạn chế

- Metrics cụ thể (NDCG, HR, AUC) và compression ratios không được công bố rõ trong abstract
- Learnable element-wise thresholds tăng hyperparameter tuning complexity
- Overhead tính toán của learnable thresholds trong inference không được phân tích
- Không nêu rõ failure cases hoặc điều kiện mà phương pháp không hoạt động tốt
- Generalization sang domains ngoài recommendation chưa được kiểm chứng
- Memory-accuracy tradeoff vẫn tồn tại, chỉ được cải thiện chứ không loại bỏ
