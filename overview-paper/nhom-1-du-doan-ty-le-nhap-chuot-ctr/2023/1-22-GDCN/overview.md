# Overview: Towards Deeper, Lighter and Interpretable Cross Network for CTR Prediction

**ArXiv ID:** [2311.04635](https://arxiv.org/abs/2311.04635)
**Venue:** CIKM 2023
**Năm:** 2023
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

- Khi tăng độ sâu (order) của feature interactions trong Cross Network, hiệu suất có xu hướng giảm — gọi là "diminishing return problem"
- Các phương pháp hiện tại không cung cấp giải thích (interpretability) cho high-order feature interactions, khiến khó hiểu decision making
- Embedding layers chứa parameter dư thừa — lãng phí tài nguyên tính toán và bộ nhớ
- DCN tập trung tăng order nhưng không giải quyết hiệu suất giảm; DeepFM, xDeepFM quá nhiều params và khó giải thích
- Chưa có phương pháp kết hợp được cả 3 mục tiêu: deeper network, lighter model, interpretability

## 2. Phương pháp sử dụng

- **Gated Cross Network (GCN):** Phát triển từ DCN, thêm "information gate" ở mỗi order — gate lọc interactions không quan trọng, chỉ giữ lại meaningful interactions
- Công thức: x_{k+1} = x_0 ⊙ (w_k^T ⊙ (x_k ⊙ x_k^T)) ⊙ g_k + x_k, với g_k là learned gate (sigmoid activation)
- Gate output ∈ [0,1] tác động như weight cho mỗi interaction; interactions yếu bị "mute", chỉ strong interactions lan truyền qua các layer
- **Field-level Dimension Optimization (FDO):** Học optimal embedding dimension cho mỗi field dựa trên importance (user_id → dimension cao, click_time → thấp)
- FDO gắn learnable scaling factor cho mỗi field, prune dimensions có importance thấp → model tự động allocate capacity hợp lý
- Gate values cung cấp insight về importance của high-order interactions, có thể visualize feature interaction graph
- Joint optimization GCN + FDO parameters với standard binary cross-entropy loss

## 3. Thành tựu đạt được

- Chỉ sử dụng 23% parameters so với DCN original nhưng đạt comparable/better performance — minh chứng model lighter hiệu quả
- Đánh giá trên 5 datasets: Criteo, Avazu, MovieLens, Frappe, Amazon — cải thiện nhất quán trên tất cả
- Outperforms DCNv2, DeepFM, xDeepFM, AutoInt trong fair comparison
- Tăng khả năng giải thích qua gate values visualization — có thể xác định feature pairs quan trọng
- Được chấp nhận tại CIKM 2023 (top-tier venue trong data mining & information retrieval)
- Code open-source: https://github.com/anonctr/GDCN

## 4. Hạn chế

- Gate mechanism khó guarantee luôn filter "correct" interactions — có thể không capture subtle interactions giữa rare features
- FDO là heuristic approach, không có chứng minh lý thuyết về optimal dimension distribution
- Gate computation ở mỗi layer thêm computational cost so với vanilla DCN (dù nhỏ)
- Chưa test trên very large-scale datasets (100B+ records) và chưa so sánh với transformer-based CTR models mới
- Interpretability vẫn không trivial trong high-dimensional space; FDO thêm hyperparameter cần tune
