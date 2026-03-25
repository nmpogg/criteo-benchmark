# Review Paper: Dissecting Embedding Bag Performance in DLRM Inference

**ArXiv ID:** [2512.05831](https://arxiv.org/abs/2512.05831)
**Năm:** 2025 (December)
**Nhóm:** 5 - Nén Embedding & Nén mô hình
**Tác giả:** Chandrish Ambati, Jing Ding, Trung Diep

---

## 1. Paper này đang nghiên cứu gì?

Paper đánh giá chi tiết hiệu suất Embedding Bag kernels trong Deep Learning Recommendation Model (DLRM) inference khi bảng embedding lớn phải phân tán trên nhiều GPU nodes. Vấn đề cơ bản: các bảng embedding hiện đại có kích thước từ vài GB đến hàng TB, vượt quá bộ nhớ single GPU. Khi phân tán, các lookups phải kích hoạt giao tiếp inter-GPU qua NCCL (NCCLCollectives) hoặc NVSHMEM (NVIDIA Shared Memory), tạo ra overhead synchronization.

Động lực: hầu hết tài liệu về DLRM tập trung vào training, ít có nghiên cứu sâu về distributed inference performance. Các engineer sản xuất cần hiểu rõ performance bottlenecks khi scale embedding tables. Khoảng trống: không có benchmark chi tiết mapping các tham số (batch size, số tables, table size, embedding dimension) tới throughput/latency thực tế trên hardware sản xuất (H100).

## 2. Phương pháp sử dụng

**Cách tiếp cận empirical measurement:**

1. **Testbed setup:** Sử dụng H100 GPUs với NCCL 2.21+ và NVSHMEM libraries. Triển khai Embedding Bag kernel trên single node multi-GPU (2, 4, 8 GPUs) để đo lường communication/computation overlap.

2. **Biến đánh giá:**
   - Batch sizes: 64, 128, 256, 512, 1024, 2048
   - Số embedding tables: 26, 128 (typical CTR models)
   - Kích thước bảng: 100K - 100M rows
   - Pooling factors: mean, sum, max pooling
   - Embedding dimensions: 16, 32, 128

3. **Giao tiếp protocols:** So sánh NCCL all-reduce (standard allreduce) vs NVSHMEM (shared memory direct access). NCCL phù hợp cho multi-node, NVSHMEM tối ưu single-node throughput.

4. **Workload mô phỏng:** Embedding lookups theo access patterns thực tế (sparse indexing theo CTR model), không dùng synthetic sequential access.

**Chiến lược phân tích:**
- Tách compute time từ communication time via kernel profiling (NVIDIA Nsight)
- Mô hình performance degradation khi scale node count
- Projection tới larger deployments dựa trên micro-benchmarks

## 3. Thành tựu đạt được

**Benchmark H100 Single-Node (2-8 GPUs):**

- **Peak embedding lookup throughput:** ~1.2M embeddings/sec (single GPU), giảm ~20-30% mỗi khi thêm GPU (tỷ lệ mở rộng sublinear)
- **NVSHMEM vs NCCL:** NVSHMEM đạt 2-3× higher throughput cho single-node (không network stack overhead)
- **Communication bottleneck:** Dominates khi batch size nhỏ (<256). Khi batch size lớn (>1024), compute-bound, communication overlap tốt hơn

**Scaling characteristics (N GPUs, fixed workload):**
- 2 GPUs: 90% efficiency vs single GPU
- 4 GPUs: 70% efficiency (communication overhead tăng)
- 8 GPUs: 45-50% efficiency (contention trên interconnect)

**Key findings:**
- Embedding dimension có impact lớn: 128-dim vs 16-dim → 3× throughput difference
- Pooling strategy ảnh hưởng: max-pool hợp lý cho sparsity, mean-pool yêu cầu full aggregation
- Table size distribution: unbalanced tables tạo straggler problems (10-15% slowdown)

**Scalability projection tới 16+ GPUs:** Hiệu suất sẽ tiếp tục suy giảm ~15-20% per doubling node count do network contention và synchronization overhead tăng.

## 4. Hạn chế

**Giới hạn đánh giá:**
- Chỉ H100 GPUs; không xét A100, L40, hoặc architecture khác với memory/interconnect khác
- Single-node multi-GPU chỉ; không đánh giá multi-node distributed inference (AddNet, DGX cluster topologies)
- Workloads dựa trên CTR models; không xét other recommendation architectures (knowledge graphs, ranking models)

**Thiếu kỹ thuật mitigation:**
- Paper chủ yếu empirical measurement; không đề xuất optimization techniques (kernel fusion, gradient reuse, quantization)
- Không so sánh với alternative sharding strategies hoặc hierarchical embedding partitioning

**Giả định:**
- Embedding tables static (không online updates); dynamic embedding invalidation không xét
- Network bandwidth giữa GPUs qua PCIe/NVLink; không xét cross-socket communication cost
- Batch arrivals independent; không xét batching under variable arrival rates

**Công việc tương lai:**
- Extend tới multi-node deployments + RoCE/InfiniBand analysis
- Optimize embedding sharding strategies dựa trên empirical findings
- Explore kernel-level optimizations (TF32 precision, mixed-precision training)
