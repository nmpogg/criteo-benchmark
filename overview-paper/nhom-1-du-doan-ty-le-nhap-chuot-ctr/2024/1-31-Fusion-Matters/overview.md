# Review Paper: Fusion Matters: Learning Fusion in Deep Click-through Rate Prediction Models

**ArXiv ID:** [2411.15731](https://arxiv.org/abs/2411.15731)
**Năm:** 2024 | **Venue:** WSDM 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo nhận thấy khoảng trống quan trọng: các mô hình CTR hiện tại dựa vào **chiến lược fusion ngây thơ** với kết nối cố định và phép toán xác định trước (sum, concat, product). Mặc dù feature interaction components được nghiên cứu kỹ lưỡng, fusion design — cách kết hợp các thành phần — lại bị bỏ qua hoàn toàn. Thay đổi fusion design có thể dẫn đến hiệu suất rất khác nhau. Không có phương pháp tự động tìm cách fusion tối ưu cho mỗi dataset.

## 2. Phương pháp sử dụng

**OptFusion** tự động hóa fusion learning qua hai cơ chế:

- **Connection Learning**: Tự động học cách kết nối giữa các modules trong mô hình (module nào nên nối với module nào)
- **Operation Selection**: Tự động chọn phép toán fusion tối ưu (sum, concat, product, attention, v.v.) cho mỗi kết nối
- Sử dụng **one-shot learning algorithm** xử lý cả hai tác vụ đồng thời — hiệu quả hơn NAS truyền thống vốn cần search space exploration tốn kém
- Loại bỏ nhu cầu thiết kế fusion thủ công, tìm cấu hình tối ưu cho từng dataset

## 3. Thành tựu đạt được

- Cải thiện hiệu suất CTR trên **3 large-scale datasets**, vượt trội các fusion designs thủ công
- Hiệu quả hơn Neural Architecture Search truyền thống về chi phí tìm kiếm
- Chấp nhận tại **WSDM 2025** — hội nghị hàng đầu web search & data mining
- Code công khai trên GitHub

## 4. Hạn chế

- Chỉ áp dụng cho CTR prediction, tính ứng dụng cho các task ML khác chưa kiểm chứng
- Chi phí one-shot learning vẫn có thể cao với datasets siêu lớn
- Thiếu so sánh trực tiếp cost-performance ratio với NAS tiên tiến (DARTS, ProxylessNAS)
- Fusion strategies học được trên dataset này chưa chắc transfer sang dataset khác
