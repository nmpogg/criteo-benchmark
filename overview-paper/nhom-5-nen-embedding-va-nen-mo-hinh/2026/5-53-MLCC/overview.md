# Review Paper: MLCC — Multi-Level Compression Cross Networks for CTR Prediction

**Tên đầy đủ:** Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems
**ArXiv ID:** [2602.12041](https://arxiv.org/abs/2602.12041)
**Tác giả:** Heng Yu, Xiangjun Zhou, Jie Xia, Heng Zhao, Anxin Wu, Yu Zhao, Dongying Kong (Bilibili)
**Năm:** 2026 (SIGIR'24)
**Code:** [shishishu/MLCC](https://github.com/shishishu/MLCC)
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

**Vấn đề cốt lõi:** Trong hệ thống CTR prediction quy mô lớn, tồn tại mâu thuẫn cơ bản giữa:
- **Kiến trúc nhẹ** (simple interaction operators như dot product): Thiếu năng lực mô hình hóa phụ thuộc phức tạp giữa features
- **Kiến trúc mạnh** (expressive architectures như Wukong): Chi phí tính toán quá lớn (415M params, 1.66TB FLOPs) và mở rộng kém

**Hiện tượng embedding collapse:** Cách tiếp cận truyền thống — tăng chiều embedding để cải thiện hiệu suất — gặp hiện tượng "embedding collapse": DNN bất động (plateau) khi E > 64, các chiều mới không cung cấp thêm thông tin hữu ích.

**Khoảng trống nghiên cứu:** Các phương pháp trước (DCNv2, Wukong, RankMixer) chủ yếu dựa vào tương tác tĩnh (fixed interaction operations) và scaling theo chiều sâu. Chưa có giải pháp kết hợp nén + tương tác động + scaling đa trục.

→ **Câu hỏi nghiên cứu:** Làm thế nào thiết kế kiến trúc tương tác feature vừa biểu diễn cao (expressive), vừa hiệu quả tính toán, vừa mở rộng tốt (scalable)?

---

## 2. Phương pháp sử dụng

### Paradigm Compress-Cross-Scale — 3 giai đoạn tuần tự:

### Giai đoạn 1: COMPRESS (Nén phân cấp)

**a) Global Compressor (GC):** Tổng hợp tất cả feature tokens thành M "global tokens" qua weighted aggregation → thu thông tin ngữ cảnh toàn cục. Ví dụ: từ hàng chục input tokens → 8-16 global tokens.

**b) Local Compressor (LC):** Áp dụng token-wise projection lên các biểu diễn đã tinh chế, tỷ lệ nén r = E_in / E_out. Ví dụ: r=4 → giảm 75% kích thước embedding mỗi token.

```
GC: M = Aggregate(x₁, x₂, ..., xₙ)     // n features gốc → M global tokens
LC: y_i = Projection(x_i)                // nén từng token với tỷ lệ r
```

### Giai đoạn 2: CROSS (Progressive Layered Crossing — PLC)

Đây là **đóng góp sáng tạo chính** của bài báo. Thay vì dùng tương tác tĩnh (dot product), PLC sử dụng tương tác động:

1. Mỗi global token m được chuyển thành **tham số của một MLP** (dynamic parameterization)
2. MLP này xử lý các token gốc → tạo cross-features bậc cao phi tuyến
3. Mỗi head = một MLP độc lập được điều kiện hóa bởi global tokens

```
Với mỗi global token m ∈ M:
    θ_m = MLP_θ(m)                    // sinh tham số động từ context
    cross_m = MLP_cross(x; θ_m)       // tương tác phi tuyến bậc cao
output = Aggregate(cross₁, ..., cross_H)  // tổng hợp H heads
```

→ **Ưu điểm:** Tạo cross-features phi tuyến bậc cao trong MỘT lớp duy nhất, thích ứng động theo context.

### Giai đoạn 3: SCALE (Mở rộng đa trục)

Ba trục scaling (khác với truyền thống chỉ tăng depth):

| Trục | Cách thức | Ý nghĩa |
|------|-----------|---------|
| **Vertical** | Tăng số PLC layers | Sâu hơn |
| **Horizontal (Heads)** | Tăng H (số MLPs độc lập) | Nhiều không gian tương tác |
| **Multi-Channel (MC-MLCC)** | Chia embeddings thành S kênh song song, mỗi kênh có GC + PLC riêng | Mở rộng hiệu quả nhất |

MC-MLCC: Mỗi kênh xử lý E/S chiều embedding → ghép kết quả S kênh → học các không gian tương tác bổ sung (complementary). Chi phí tăng tuyến tính với S (không bình phương).

---

## 3. Thành tựu đạt được

### Kết quả trên tập dữ liệu công khai (AUC):

| Dataset | Quy mô | MC-MLCC | Wukong | Cải thiện |
|---------|--------|---------|--------|-----------|
| **Criteo** | 45M mẫu | **0.8034** | 0.8013 | +0.21% |
| **Avazu** | 40M mẫu | **0.7945** | 0.7893 | +0.52% |
| **TaobaoAds** | 26M mẫu | **0.6596** | 0.6568 | +0.28% |

### Kết quả trên dữ liệu công nghiệp (Bilibili) — điểm nhấn chính:

| Mô hình | AUC | Tham số | FLOPs |
|---------|-----|---------|-------|
| DNN (baseline) | 0.8295 | 127M | 512GB |
| DCNv2 | 0.8327 | 89M | 356GB |
| Wukong (SOTA cũ) | 0.8334 | 415M | 1.66TB |
| **MLCC** | **0.8333** | 65.2M | 268GB |
| **MC-MLCC** | **0.8334** | **15.5M** | **64.9GB** |

→ MC-MLCC đạt **cùng AUC với Wukong** nhưng với **26× ít tham số** (15.5M vs 415M) và **26× ít FLOPs** (64.9GB vs 1.66TB).

### Scaling laws — giải quyết embedding collapse:

| Embedding Dim | DNN (AUC) | MLCC (AUC) | Ghi chú |
|---------------|-----------|------------|---------|
| E = 64 | 0.8323 | 0.8326 | DNN bắt đầu plateau |
| E = 128 | 0.8324 | 0.8330 | DNN bất động, MLCC vẫn tăng |
| E = 256 | 0.8323 | 0.8332 | MLCC tiếp tục cải thiện |

→ DNN gặp embedding collapse từ E > 64, MLCC tiếp tục cải thiện tuyến tính đến E = 256.

MC-MLCC (E=16, S=16) đạt AUC tương đương MLCC (E=192) nhưng với **4× ít tham số** → mở rộng theo kênh hiệu quả hơn nhiều so với tăng embedding dimension.

### Triển khai thực tế (Online A/B Testing tại Bilibili):
- **ADVV (Ad View Value):** +32%
- **Latency:** < 20ms (tuân thủ production constraints)
- **Trạng thái:** Đã triển khai rộng rãi trong hệ thống quảng cáo Bilibili

---

## 4. Hạn chế

### Hạn chế về kết quả:
- **Cải thiện AUC nhỏ trên tập công khai:** Avazu +0.52%, Criteo +0.21% — mặc dù có ý nghĩa thống kê nhưng mức cải thiện tương đối rất nhỏ (0.026-0.065%)
- **Dữ liệu công nghiệp không công khai:** Kết quả ấn tượng nhất (Bilibili) không thể tái tạo và xác minh độc lập
- **Baseline chưa đầy đủ:** Chủ yếu so sánh với Wukong, DCNv2, DNN — thiếu so sánh với các phương pháp attention-based gần đây

### Hạn chế về kỹ thuật:
- **Độ phức tạp triển khai:** MC-MLCC đòi hỏi cân bằng tải cẩn thận giữa các channels; dynamic MLPs phức tạp hơn static dot product → chi phí bảo trì production cao hơn
- **Interpretability kém:** Tương tác phi tuyến động khó giải thích tại sao mô hình đưa ra quyết định cụ thể — vấn đề quan trọng trong quảng cáo/tín dụng
- **Nhiều hyperparameters mới:** compression ratio (r), số heads (H), số channels (S), kích thước MLP ẩn → khó tìm cấu hình tối ưu cho dataset mới
- **Chưa thảo luận chi phí bộ nhớ GPU trong training** — MC-MLCC variant có thể yêu cầu bộ nhớ lớn hơn đáng kể

### Hạn chế về lý thuyết:
- **Không có chứng minh lý thuyết** về sức mạnh biểu diễn — PLC có thể học được TẤT CẢ tương tác bậc cao hay không?
- **Không có phân tích convergence** — dynamic MLPs có thể gây khó khăn cho quá trình tối ưu hóa
- **Scaling laws chỉ phân tích chi tiết trên Bilibili** — thiếu phân tích trên các tập công khai
- **Không thảo luận failure cases** — chưa rõ đặc điểm dữ liệu nào ảnh hưởng đến hiệu suất MLCC
