# Review Paper: Legend - Efficient Graph Embedding at Scale: Optimizing CPU-GPU-SSD Integration

**ArXiv ID:** [2505.09258](https://arxiv.org/abs/2505.09258)
**Năm:** 2026 (VLDB Journal)
**Nhóm:** 5 - Nén Embedding & Nén mô hình
**Tác giả:** Zhonggen Li, Xiangyu Ke, Yifan Zhu, Yunjun Gao, Feifei Li

---

## 1. Paper này đang nghiên cứu gì?

Legend giải quyết vấn đề mở rộng quy mô trong huấn luyện graph embedding cho các đồ thị miliárd-scale (billion-scale). Các phương pháp hiện tại gặp phải đilemma: hoặc yêu cầu GPU memory khổng lồ (không khả thi về kinh tế) hoặc chịu đựng độ trễ I/O lớn từ truy cập disk. Cụ thể, các hệ thống hiện tại như GE2 yêu cầu 4 GPU để xử lý Twitter graph (1.3B cạnh, 41.6M node), trong khi Marius chỉ dùng 1 GPU nhưng tốc độ chậm hơn 4.8 lần do I/O overhead.

Động lực chính: graph embeddings là nền tảng cho community detection, recommendation systems, và nhiều ứng dụng khoa học. Tuy nhiên, không có hệ thống nào hiệu quả đạt được cân bằng giữa chi phí phần cứng, throughput, và efficiency. Khoảng trống nghiên cứu rõ ràng là thiếu phương pháp khai thác hiệu quả hệ thống CPU-GPU-SSD heterogeneous trong bối cảnh embedding training.

## 2. Phương pháp sử dụng

Legend triển khai hệ thống three-tiered heterogeneous: NVMe SSD lưu trữ node embeddings và optimizer states (dữ liệu lớn), Host RAM giữ edges theo buckets và graph topology, GPU global memory chứa relation embeddings, optimizer states, và buffer cho node partitions.

**Thuật toán chính:**

1. **Edge Bucket Ordering (Prefetch-Friendly Loading):** Giải quyết vấn đề overlap I/O-compute. Phương pháp truyền thống không thể overlap vì phải chờ partition load từ SSD. Legend sử dụng "column separation covering strategy" để sinh thứ tự loading thoả mãn: (i) partitions swapped gần đây không bị evict ngay, (ii) bất kỳ cặp partition nào chỉ xuất hiện liên tiếp trong buffer states. Thuật toán heuristic giải NP-hard problem trong <1 giây.

2. **Customized GPU-SSD Direct-Access Driver:** Loại bỏ trung gian CPU. Sử dụng: (i) precomputed queue positions cho lock-free concurrent enqueue/dequeue, (ii) full-coalesced doorbell ringing, (iii) batch polling. Đạt 3.06 GB/s SSD-GPU bandwidth (Bảng 1).

3. **GPU Computation Optimization:** Tận dụng Tensor cores + CUDA cores cho batch computation, giảm memory access qua register/shared memory, reuse intermediate results. Đạt 7.18×10⁶ edges/sec throughput.

**Kiến trúc quyết định:**
- **Partition-based storage:** Memory layout liên tiếp cho phép load simultaneously embedding+optimizer via single GPU kernel
- **RAM-resident edges:** CPU track GPU progress, transfer buckets synchronously (3× higher bandwidth vs SSD-GPU)
- **CUDA streams parallelism:** Overlap data-access kernels với compute kernels
- **GPU buffer = 3 partitions:** Cân bằng memory constraints với prefetch opportunities

## 3. Thành tựu đạt được

**Trên Twitter graph (1.3B cạnh, 41.6M node):**

| Metric | GE2 (4 GPUs) | Marius (1 GPU) | Legend (1 GPU) |
|--------|--------------|----------------|----------------|
| Batch time | 18.5 ms | 315.6 ms | 12.0 ms |
| Total time | 32 min | 146 min | 30 min |
| Speedup | baseline | 4.8× (vs Marius) | **parity với GE2** |
| Storage cost | $2.02/GB | $0.13/GB | $0.13/GB |

**Kết quả chính:**
- Đạt hiệu suất tương đương 4-GPU GE2 nhưng chỉ dùng 1 GPU
- **4.8× speedup** so với Marius (hệ thống single-GPU trước đó)
- Chi phí lưu trữ giữ nguyên thấp ($0.13/GB)
- I/O overhead giảm từ >80% batch time xuống mức overlap hiệu quả

**Chi tiết hiệu suất:**
- SSD-GPU bandwidth: 3.06 GB/s (vs CPU-GPU: ~200 MB/s truyền thống)
- GPU throughput: 7.18×10⁶ edges/sec
- CPU-centric batch construction overhead loại bỏ (26× slowdown trong Marius)

## 4. Hạn chế

- **Phụ thuộc phần cứng:** Thiết kế tối ưu cho NVMe SSD hiệu suất cao. Khả năng mở rộng trên SSD tốc độ thấp hoặc HDD không được đánh giá.
- **Đồ thị cụ thể:** Chỉ đánh giá trên Twitter graph. Tính chung chung cho các cấu trúc đồ thị khác (power-law khác, density khác, distribution khác) chưa rõ ràng.
- **Scaling limitation:** Chỉ đánh giá single-GPU. Khả năng multi-GPU cluster không được thảo luận.
- **Giả định:** Edge metadata phải vừa trong Host RAM; không áp dụng cho graphs với edge metadata lớn.
- **Overhead setup:** Column covering heuristic chạy offline; nếu graph thay đổi thường xuyên, overhead này có thể trở nên đáng kể.
