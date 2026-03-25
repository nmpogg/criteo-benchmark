# Review Paper: MLKV: A Disk-based Key-Value Store for Large Embedding Model Training

**ArXiv ID:** [2504.01506](https://arxiv.org/abs/2504.01506)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết tính khả mở rộng trong huấn luyện các mô hình embedding lớn:
- Tập hợp các tối ưu hóa vào một hệ thống KV dựa trên đĩa cứng thống nhất
- Xử lý "data stall" và "staleness"

## 2. Phương pháp sử dụng

- Disk-based key-value storage để xử lý data stall và staleness
- Interfaces thiết kế đặc biệt cho training embedding models
- Công khai hóa tính năng trước đó độc quyền

## 3. Thành tựu đạt được

- Hiệu suất vượt trội: 1.6-12.6x tốt hơn trên open-source workloads
- Thử nghiệm thành công trên hệ thống thực tế từ eBay (payment risk detection)
- Code open-source

## 4. Hạn chế

- Disk-based storage có thể gây trade-off latency so với in-memory approaches
- Cần đọc full paper để biết hạn chế chi tiết
