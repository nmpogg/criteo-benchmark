# Review Paper: MPE: Mixed-Precision Embeddings for Large-Scale Recommendation Models

**ArXiv ID:** [2409.20305](https://arxiv.org/abs/2409.20305)
**Năm:** 2024
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Embedding tables trong recommendation systems chiếm memory rất lớn, gây thách thức cho deployment quy mô lớn. Paper nhận thấy không phải tất cả embeddings đều quan trọng bằng nhau — một số features có tác động lớn hơn đến prediction. Vấn đề là làm sao nén embedding tables mà không mất accuracy, đồng thời tận dụng sự khác biệt về tầm quan trọng giữa các features.

**Motivation:** Áp dụng precision levels khác nhau cho từng nhóm features — features quan trọng dùng high precision, features ít quan trọng dùng low precision — để đạt compression ratio cao mà giữ quality.

## 2. Phương pháp sử dụng

**Mixed-Precision Embeddings (MPE):**

1. **Feature Grouping:** Tổ chức features theo tần suất xuất hiện để giảm search space complexity
2. **Probability Learning:** Học phân phối xác suất trên nhiều mức precision cho từng nhóm features — tự động xác định precision tối ưu
3. **Sampling Strategy:** Cơ chế sampling chuyên biệt để xác định gán precision tối ưu cho mỗi feature
4. **Dynamic Quantization:** Quantization động với precision levels được điều chỉnh theo feature importance — không cần fixed precision cho toàn bộ table

## 3. Thành tựu đạt được

| Metric | Kết quả |
|--------|---------|
| **Compression ratio** | ~200× trên Criteo dataset |
| **Accuracy** | Không giảm so với baseline |
| **Comparison** | Vượt trội các phương pháp compression hiện có trên 3 public datasets |

Phương pháp chứng minh rằng mixed-precision approach hiệu quả hơn uniform quantization.

## 4. Hạn chế

- **Feature distribution dependency:** Hiệu quả phụ thuộc vào phân bố features — nếu distribution quá heterogeneous, grouping strategy có thể không tối ưu
- **Search overhead chưa rõ:** Chi phí tính toán của probability learning và sampling chưa được chi tiết hóa
- **Limited datasets:** Chỉ kiểm nghiệm trên 3 datasets, chưa validate trên production-scale systems
- **Under submission:** Paper chưa được peer-reviewed tại venue chính thức
- **Scalability:** Chưa rõ performance khi số lượng features tăng lên hàng tỷ
