# Review Paper: DimGrow: Progressive Embedding Dimension Growing for Recommendation Systems

**ArXiv ID:** [2505.12683](https://arxiv.org/abs/2505.12683)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết vấn đề phân bổ tự động chiều embedding trên các trường dữ liệu khác nhau:
- Thay vì sử dụng kích thước cố định cho tất cả

## 2. Phương pháp sử dụng

- Khởi tạo mô hình với chiều embedding tối thiểu (1 chiều per field)
- Sử dụng importance scoring để xác định trường nào cần mở rộng
- Mở rộng chiều động khi importance vượt ngưỡng
- Tránh tạo SuperNet đắt đỏ (memory-intensive)

## 3. Thành tựu đạt được

- Tối ưu hóa thành công chiều embedding ở cấp trường (field-level)
- Giảm memory tiêu tốn khi training so với SuperNet truyền thống
- Hiệu quả trên 3 datasets khuyến nghị

## 4. Hạn chế

- Chưa có chi tiết về hiệu suất định lượng cụ thể
- Chỉ kiểm chứng trên miền khuyến nghị
- Không cung cấp so sánh chi tiết về độ chính xác/hiệu năng
