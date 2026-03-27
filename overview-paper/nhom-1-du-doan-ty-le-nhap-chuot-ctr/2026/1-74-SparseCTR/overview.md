# Review Paper: SparseCTR — Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction

**ArXiv:** [2601.17836](https://arxiv.org/abs/2601.17836) | **Năm:** 2026 | **Venue:** WWW 2026
**Tác giả:** Weijiang Lai, Beihong Jin, Di Zhang, Siru Chen, Jiongyan Zhang, Yuhang Gou, Jian Dong, Xingxing Wang

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **triển khai scaling-law models cho CTR prediction** trong hệ thống recommendation thực tế, tập trung vào xử lý **long-term user behaviors** hiệu quả:

- **Challenge triển khai:** Scaling laws cho thấy models lớn hơn → performance tốt hơn, nhưng full attention trên long behavior sequences (>1000 items) có O(n²) complexity → không thể serve trong latency constraints (<50ms).
- **Sparse attention chưa được khai thác:** Sparse attention đã thành công trong NLP (Longformer, BigBird) nhưng chưa được thiết kế riêng cho CTR — user behaviors có đặc thù khác text (temporal patterns, periodic interests, multi-granularity).
- **Mất continuous patterns:** Các sparse attention methods thông thường (fixed patterns, random) có thể phá vỡ continuous behavior patterns quan trọng (ví dụ: chuỗi mua sắm liên tiếp trong 1 session).

## 2. Phương pháp sử dụng

**SparseCTR** — sparse attention thiết kế riêng cho CTR với 3 thành phần:

**1. Personalized Chunking:**
- Phân chia behavior sequence thành **chunks theo cách riêng từng user** thay vì fixed-size chunks
- Dựa trên **temporal boundaries** (session breaks, time gaps) và **behavioral coherence** (chuỗi hành vi cùng chủ đề)
- Bảo tồn continuous patterns trong mỗi chunk → không phá vỡ session logic
- Cho phép **parallel processing** giữa các chunks → tăng throughput

**2. Three-Branch Sparse Attention:**
Capture 3 khía cạnh khác nhau của user interest:
- **Branch 1 — Global Interest:** Attention trên representative tokens từ mỗi chunk → capture long-term general preferences
- **Branch 2 — Interest Transition:** Attention giữa boundary tokens của chunks liền kề → capture sự chuyển đổi sở thích qua thời gian
- **Branch 3 — Short-term Interest:** Dense attention trong chunk gần nhất → capture immediate preferences

**3. Composite Relative Temporal Encoding:**
- Sử dụng **learnable head-specific bias coefficients** — mỗi attention head có temporal encoding riêng
- Capture cả **sequential relationships** (item A trước item B) và **periodic relationships** (user mua sữa mỗi tuần)
- Cho phép mô hình phân biệt "cách đây 1 phút" vs "cùng thời điểm tuần trước"

## 3. Thành tựu đạt được

- **Online A/B testing thành công:**
  - **+1.72% CTR improvement**
  - **+1.41% CPM improvement** (Cost Per Mille)
  - Improvements đáng kể trong industrial setting
- **Scaling law consistency:** Lợi ích scaling đều đặn qua **3 orders of magnitude trong FLOPs** (10× → 100× → 1000× compute)
- **Vượt trội SOTA methods** trên cả offline metrics và online A/B testing
- **Accepted tại WWW 2026** — hội nghị top-tier
- **Code công khai** trên GitHub — reproducible

## 4. Hạn chế

- **Personalized chunking phức tạp:** Cần xác định boundary criteria cho từng user → logic phức tạp trong production serving pipeline
- **Per-user chunking overhead:** Mỗi user có chunking strategy khác nhau → khó batch processing, ảnh hưởng throughput
- **Three branches tăng memory:** 3 attention branches song song × multi-head = memory footprint đáng kể
- **Generalization cross-domain:** Chunking criteria và temporal encoding được thiết kế cho e-commerce — chưa rõ hiệu quả trên video, news, social media
- **Periodic pattern assumption:** Composite temporal encoding giả định có periodic behaviors — users không có patterns rõ ràng có thể không benefit
