# Review Paper: Legend: Efficient Graph Embedding Training with GPU-SSD Memory Hierarchy

**ArXiv ID:** [2505.09258](https://arxiv.org/abs/2505.09258)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết vấn đề mở rộng quy mô trong hệ thống graph embedding:
- Hoặc sử dụng GPU memory khổng lồ hoặc chịu độ trễ I/O lớn
- Cung cấp giải pháp tối ưu cho graph embedding tỷ độ (billion-scale)

## 2. Phương pháp sử dụng

- Prefetch-friendly embedding-loading order
- Custom GPU-SSD direct-access driver cho embedding access patterns
- Parallel execution optimization: tối đa GPU utilization

## 3. Thành tựu đạt được

- Tăng tốc end-to-end workloads 4.8x so với state-of-the-art
- Đạt hiệu suất tương đương competitor trên largest workloads với chỉ 1/4 số lượng GPUs

## 4. Hạn chế

- Trade-offs giữa CPU-GPU-SSD; khả năng mở rộng trên các cấu hình phần cứng khác chưa rõ
- Có thể không tổng quát hóa cho các loại graph khác
