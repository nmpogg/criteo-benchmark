# Review Paper: Helen: Optimizing CTR Prediction Models with Frequency-wise Hessian Eigenvalue Regularization

**ArXiv ID:** [2403.00798](https://arxiv.org/abs/2403.00798)
**Năm:** 2024 | **Venue:** WWW 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo tiếp cận CTR prediction từ góc độ tối ưu hóa thay vì kiến trúc mô hình. Tác giả phát hiện vấn đề cơ bản: các features xuất hiện thường xuyên (high-frequency features) có xu hướng hội tụ về **sharp local minima** trên loss landscape, làm suy giảm hiệu suất generalization. Đây là vấn đề về cảnh quan hàm mất mà các optimizers truyền thống (Adam, SGD) không xử lý được — chúng không phân biệt giữa features có tần suất khác nhau.

## 2. Phương pháp sử dụng

Helen là một **optimizer chuyên biệt** kết hợp:

- **Hessian eigenvalue regularization theo tần suất**: Ràng buộc top eigenvalue của ma trận Hessian cho từng feature dựa trên tần suất xuất hiện — features xuất hiện nhiều bị regularize mạnh hơn
- **Adaptive perturbations**: Nhiễu loạn thích ứng được điều chỉnh theo tần suất feature chuẩn hóa, lấy cảm hứng từ **Sharpness-Aware Minimization (SAM)**
- Khuyến khích mô hình khám phá vùng loss landscape phẳng hơn (flat minima), cải thiện generalization
- Kiểm tra trên **7 mô hình CTR phổ biến**, **3 benchmark datasets** trong framework BARS

## 3. Thành tựu đạt được

- Thành công ràng buộc top Hessian eigenvalue, chứng minh giả thuyết về sharp minima
- Vượt trội các optimizers chuẩn trên framework đánh giá BARS
- Chấp nhận tại **WWW 2024** (ACM Web Conference) — hội nghị hàng đầu
- Code công khai trên GitHub, hỗ trợ reproducibility

## 4. Hạn chế

- Chỉ kiểm thử trên CTR prediction, generalization sang ranking/recommendation khác chưa rõ
- Chi phí tính toán Hessian eigenvalue có thể là bottleneck trên datasets cực lớn
- Thiếu so sánh với các flat minima optimizers khác (ASAM, LookSAM, v.v.)
- Không phân tích chi tiết tác động Hessian computation trên các kiến trúc model khác nhau
- Cải thiện định lượng cụ thể (% AUC gain) không được nêu rõ trong abstract
