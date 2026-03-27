# Review Paper: MLKV: Efficiently Scaling up Large Embedding Model Training with Disk-based Key-Value Storage

**ArXiv ID:** [2504.01506](https://arxiv.org/abs/2504.01506)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết vấn đề khả năng mở rộng trong training các large embedding models. Các ứng dụng hiện đại như Deep Learning Recommendation Models (DLRMs), Knowledge Graph Embeddings (KGEs), và Graph Neural Networks (GNNs) cần lưu trữ và truy cập hàng tỷ embedding vectors. Kích thước các embedding tables thường vượt quá bộ nhớ GPU có sẵn (hoặc thậm chí single machine), gây ra bottleneck đáng kể trong training pipelines.

Vấn đề chính là **data stall** - GPUs idle waiting cho disk I/O khi accessing larger-than-memory embeddings - và **staleness** - khi multiple workers update embeddings asynchronously, consistency giữa các updates có thể bị compromise. Các phương pháp hiện tại hoặc không support larger-than-memory workloads, hoặc có performance overhead lớn (1.6-12.6x slowdown) khi offloading tới generic key-value stores.

Paper nhằm develop unified framework consolidate storage optimization approaches scattered across specialized frameworks, democratize optimizations trước đó exclusive tới individual systems, cung cấp 1.6-12.6× speedup over industrial key-value stores.

## 2. Phương pháp sử dụng

MLKV implement architecture trên top of FASTER - log-structured key-value store. Framework separate storage management từ application logic qua clean interfaces, cho phép ML applications invoke key-value operations cho embedding access mà không cần extensive code rewrites.

**Bốn primary interfaces:**
- **Open():** Initialize embedding models với configurable staleness bounds và dimensions
- **Get():** Retrieve embedding vectors cho forward propagation
- **Put():** Update embedding vectors during backward propagation
- **Lookahead():** Asynchronously preload embeddings vượt quá staleness constraints

**Data Stall Prevention via Look-ahead Prefetching:**
Look-ahead mechanism bring embeddings "beyond staleness bounds từ disk vào storage system's buffer pool ahead of time," enabling simultaneous computation và data movement mà không violate consistency guarantees. Prefetching strategy overlap I/O latency với GPU computation, significantly reducing idle time.

**Staleness Handling - Bounded Staleness Consistency:**
Framework implement bounded staleness consistency via per-embedding vector clocks. Users configure staleness bounds operate trong ba modes:
- **BSP (staleness_bound = 0):** Fully synchronous training - strict consistency
- **SSP (configurable bounds):** Stale Synchronous Parallel - trade consistency cho throughput
- **ASP (staleness_bound = infinity):** Fully asynchronous training - maximum throughput

MLKV achieve này sử dụng latch-free atomic operations "steal unused bits trong record-level locks để indicate staleness" mà không performance penalties cho synchronous workloads.

**Unified Storage Interface:**
Key innovation là abstraction layer unify storage operations across different ML tasks. Instead của custom offloading code cho mỗi framework, MLKV cung cấp generic put/get interface. Mô hình agnostic - applications only interact với key-value operations, storage layer handle compression, caching, consistency details.

## 3. Thành tựu đạt được

**Larger-than-memory workloads:** MLKV outperform offloading strategies built on industrial-strength key-value stores:
- **1.08-12.57× throughput improvements** across DLRM, KGE, GNN tasks so với FASTER, RocksDB, WiredTiger
- **Specific results:**
  - DLRM: 2.1× vs FASTER
  - KGE: 12.57× vs RocksDB
  - GNN: 1.08× vs specialized graph systems

**In-memory workloads:** Within 2.5-22.2% performance gap so với specialized frameworks while maintaining reusability across tasks.

**Staleness tradeoffs:**
- **Up to 6.58× speedup** with <0.1% model quality degradation when appropriately relaxing staleness bounds
- **NoSQL overhead:** <10% performance gap cho uniform access patterns; <20% cho skewed patterns
- **Real-world deployment:** eBay workloads đạt 69.6% throughput of distributed baselines using single-instance MLKV deployment

**Benchmark datasets:** Yahoo! Learning to Rank (LTR) datasets, recommendation datasets, knowledge graph datasets. Training time reduction significant khi so với baseline storage approaches.

## 4. Hạn chế

Framework phụ thuộc vào FASTER implementation - performance sensitive tới underlying log-structured store design. NoSQL overhead (10-20%) vẫn significant cho applications strict latency requirements. Staleness bounds configuration manual - không smart mechanism tự-adapt bounds dựa trên workload characteristics.

Vector clock approach có scalability challenges trên very large distributed systems - per-embedding metadata được maintain có thể become overhead. Paper không thoroughly analyze storage overhead của maintaining clocks, indices, bloom filters trên disk. Compression strategies không deeply explored - MLKV assumes embeddings stored as raw vectors.

Benchmark tập trung vào batch training - interactive/online serving scenarios not extensively studied. Integration với modern embedding quantization techniques hoặc advanced memory hierarchies (NVMe tiering) không discuss. Future work needed để investigate adaptive staleness adjustment, learned prefetch strategies using ML models, support cho GPU-efficient sketching techniques, và hybrid memory hierarchies combining DRAM, NVMe, HDD efficiently.
