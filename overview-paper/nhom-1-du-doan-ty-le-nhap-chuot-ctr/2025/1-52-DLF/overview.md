# Review Paper: DLF: Enhancing Explicit-Implicit Interaction via Dynamic Low-Order-Aware Fusion for CTR Prediction

**ArXiv ID:** [2505.19182](https://arxiv.org/abs/2505.19182)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Tập trung vào cân bằng tương tác đặc trưng tường minh với tương tác ẩn:
- Xử lý vấn đề dữ liệu thưa thớt
- Giải quyết dự đoán CTR trong quảng cáo và hệ thống khuyến nghị

## 2. Phương pháp sử dụng

- RLI (Residual-Aware Low-Order Interaction Network): bảo tồn tín hiệu cấp thấp, giảm thừa dư từ residual connections
- NAF (Network-Aware Attention Fusion Module): tích hợp động biểu diễn tường minh và ẩn qua các tầng
- Cân bằng giữa explicit feature interactions và implicit patterns

## 3. Thành tựu đạt được

- Hiệu suất state-of-the-art trong CTR prediction
- Code công khai trên GitHub
- Công bố tại SIGIR '25

## 4. Hạn chế

- Chưa chi tiết các điểm yếu cụ thể
- Không rõ hiệu suất trên các domain hoặc loại dữ liệu khác nhau
- Độ cải thiện định lượng trên benchmark chưa chi tiết
