# Review Paper: HEAM: Heterogeneous Memory Architecture for PIM-based Embedding Acceleration

**ArXiv ID:** [2402.04032](https://arxiv.org/abs/2402.04032)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding layers chiếm 90%+ thời gian truy cập bộ nhớ trong DLRM. Các thuật toán nén weight-sharing (QR-trick, TT-Rec) giảm memory nhưng tạo **sparse, irregular memory access patterns** — gây căng thẳng cho hệ thống bộ nhớ truyền thống. Paper nghiên cứu tối ưu hóa ở **tầng hardware** bằng kiến trúc Processing-In-Memory (PIM) để tăng tốc embedding lookups.

**Motivation:** Thay vì chỉ nén ở tầng algorithm, giải quyết bottleneck ở tầng hardware — đưa computation đến gần data hơn bằng PIM, giảm data movement giữa CPU/GPU và memory.

## 2. Phương pháp sử dụng

**ProactivePIM — Heterogeneous HBM-DIMM Architecture:**

1. **Two-level PIM System:**
   - **Base-die PIM (bd-PIM):** Xử lý phép toán nặng tại base die của HBM
   - **Bank-group PIM (bg-PIM):** Hoạt động ở cấp bank-group để khai thác parallelism

2. **Heterogeneous Memory:** Kết hợp High Bandwidth Memory (HBM) với DIMM truyền thống qua PIM architecture

3. **Optimization Techniques:**
   - **SRAM caching:** Tối ưu locality cho hot embeddings
   - **Subtable duplication:** Giảm CPU-PIM communication overhead
   - **Intra-GnR locality exploitation:** Khai thác tính chất đặc thù của thuật toán weight-sharing

## 3. Thành tựu đạt được

| Algorithm | Speedup |
|-----------|---------|
| **QR-trick** | 2.22× so với baseline |
| **TT-Rec** | 2.15× so với baseline |

Giải quyết hiệu quả irregular memory access patterns — bottleneck chính của weight-sharing compression.

## 4. Hạn chế

- **Hardware-specific:** Phụ thuộc phần cứng PIM chuyên dụng — không dễ tiếp cận trên hệ thống thông thường
- **Limited algorithm scope:** Chỉ đánh giá trên 2 thuật toán weight-sharing (QR-trick, TT-Rec), chưa test với hashing hay quantization
- **Cost barrier:** Chi phí phát triển và tích hợp phần cứng PIM còn cao
- **Communication overhead:** Overhead giao tiếp CPU-PIM không thể hoàn toàn loại bỏ
- **Scalability:** Khả năng mở rộng đến embedding tables cực lớn (terabyte-scale) chưa được xác nhận
