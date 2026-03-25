# Review Paper: Lossless Embedding Compression via Spherical Coordinates

**Tên đầy đủ:** Lossless Embedding Compression via Spherical Coordinates
**ArXiv ID:** [2602.00079](https://arxiv.org/abs/2602.00079)
**Tác giả:** Han Xiao (Jina AI)
**Năm:** 2026 (ICLR 2026 Workshop on Geometry-grounded Representation Learning)
**Code:** [jina-ai/jzip-compressor](https://github.com/jina-ai/jzip-compressor)
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

**Vấn đề:** Embedding vectors từ các mô hình neural (text, image, multi-vector) yêu cầu storage khổng lồ — ví dụ ColBERT index với 1 triệu tài liệu cần ~240 GB. Việc lưu trữ và truyền tải các vector này là bottleneck lớn trong hệ thống retrieval quy mô lớn.

**Khoảng trống nghiên cứu:** Hiện tại có 2 hướng tiếp cận chính nhưng đều có nhược điểm rõ ràng:
- **Lossless compression** (zstd, Blosc...): Giữ nguyên chính xác nhưng chỉ đạt ~1.2× compression ratio — quá thấp
- **Lossy quantization** (ECF8, DFloat11...): Đạt 4×+ compression nhưng mất thông tin semantic, ảnh hưởng chất lượng retrieval

**Insight cốt lõi:** Tác giả phát hiện rằng unit-norm embeddings (vector có chuẩn = 1) trong không gian cao chiều có tính chất hình học đặc biệt: khi chuyển sang tọa độ cầu (spherical coordinates), các góc θ tập trung xung quanh π/2. Điều này gây ra:
- IEEE 754 floating-point exponents suy biến (collapse) thành 1-2 giá trị duy nhất
- High-order mantissa bits trở nên có tính dự đoán cao (predictable)
- Cả hai thành phần đều rất phù hợp cho entropy coding

→ **Mục tiêu**: Khai thác tính chất hình học này để nén lossless đạt 1.5× — lấp khoảng trống giữa lossless (1.2×) và lossy (4×+).

---

## 2. Phương pháp sử dụng

### Pipeline nén (hoàn toàn deterministic, không cần training):

```
Unit-norm Embedding (Cartesian, d chiều)
    ↓
[1] Spherical Coordinate Transform → (r=1, θ₁, θ₂, ..., θ_{d-1})
    ↓
[2] Loại bỏ radial component (r luôn = 1 cho unit-norm)
    ↓
[3] Transpose — nhóm các giá trị angle tương tự lại gần nhau
    ↓
[4] Byte Shuffle — tách exponent bytes ra khỏi mantissa bytes
    ↓
[5] Entropy Coding (zstd) — nén exponents suy biến + mantissa có tương quan
    ↓
Compressed Data
```

### Chi tiết từng bước:

**Bước 1 - Spherical Coordinate Transform:** Chuyển vector Cartesian d-chiều thành d-1 góc cầu. Do vector unit-norm nên thành phần radial r = 1 → loại bỏ, tiết kiệm ngay 1 chiều.

**Bước 2 & 3 - Transpose + Byte Shuffle:** Sắp xếp lại các byte từ IEEE 754 floats:
- Exponent bytes: thường chỉ có 1-2 giá trị duy nhất (do các góc tập trung quanh π/2) → tỷ lệ nén cực cao
- Mantissa bytes: có tương quan cao giữa các góc liên tiếp → entropy encoder khai thác hiệu quả

**Bước 4 - Entropy Coding:** Sử dụng zstd (hoặc entropy coder khác) để nén final byte stream.

### Đặc điểm quan trọng:
- **Không cần training** — phương pháp hoàn toàn deterministic, không cần codebook hay learned parameters
- **Hỗ trợ streaming decompression** — không cần giải nén toàn bộ trước khi tính toán
- **Tính similarity trực tiếp từ spherical angles** — cho phép early termination trong top-k retrieval

---

## 3. Thành tựu đạt được

### Kết quả nén chính:

| Metric | Giá trị |
|--------|---------|
| Compression ratio | **1.5×** (tốt hơn 25% so với best lossless trước đó ~1.2×) |
| Reconstruction error | **< 1e-7** (dưới machine epsilon float32 ≈ 1.19e-7) |
| Error so với mantissa truncation | **10× thấp hơn** ở cùng compression ratio |

### Quy mô thực tế:
- **ColBERT index (1M docs):** 240 GB → 160 GB → tiết kiệm 80 GB (33% reduction)
- **Chất lượng retrieval:** Không suy giảm (sai số < machine epsilon → hiệu quả tương đương lossless)

### Benchmark:
- Kiểm thử trên **26 cấu hình embedding** khác nhau:
  - **Text embeddings:** Jina embeddings v3, v4 (768, 1024, 2048 chiều)
  - **Image embeddings:** Jina CLIP v1, v2
  - **Multi-vector embeddings:** Các cấu hình đa chiều
- Nhất quán đạt 1.5× trên tất cả cấu hình

### So sánh với baselines:

| Phương pháp | Loại | Compression Ratio | Mất mát |
|-------------|------|-------------------|---------|
| Blosc, ZSTD | Lossless chung | ~1.1-1.2× | Không |
| Prior lossless best | Lossless embedding | ~1.2× | Không |
| **Spherical (đề xuất)** | **Lossless** | **1.5×** | **< 1e-7** |
| ECF8, DFloat11 | Lossy | 4×+ | Có (mất semantic) |
| Mantissa truncation | Lossy | ~1.5× | 10× cao hơn đề xuất |

---

## 4. Hạn chế

### Hạn chế về phạm vi áp dụng:
- **Chỉ hiệu quả cho unit-norm embeddings** — vector chưa được normalize thì tính chất hình học không còn đúng, compression ratio sẽ giảm đáng kể
- **Tối ưu cho float32 IEEE 754** — cần điều chỉnh cho float16 hoặc bfloat16
- **1.5× là điểm cân bằng tối ưu** — không thể nén cao hơn mà vẫn giữ lossless

### Hạn chế về đánh giá:
- **Kiểm thử chủ yếu trên Jina embeddings** — chưa xác nhận với các embedding models khác (OpenAI, Cohere, Sentence-BERT...)
- **Chưa đánh giá trên non-retrieval tasks** — hiệu quả với clustering, classification, hoặc CTR/recommendation chưa rõ
- **Không thảo luận peak memory usage** khi decompression — quan trọng cho edge/embedded deployment

### Hạn chế về phương pháp:
- **Phụ thuộc entropy encoder** — hiệu suất cuối cùng phụ thuộc zstd; encoder khác cho kết quả khác
- **Không có adaptive compression** — cố định pipeline, không tự điều chỉnh theo đặc tính embedding cụ thể
- **Khả năng song song hóa** — streaming hỗ trợ nhưng full parallelization chưa được nghiên cứu kỹ
