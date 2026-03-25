# Review Paper: FedPDD: A Privacy-Preserving Double Distillation Framework for Cross-Silo Federated Recommendation

**ArXiv ID:** [2305.06272](https://arxiv.org/abs/2305.06272)
**Năm:** 2023 | **Venue:** IJCNN 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Federated learning cho recommendation systems gặp thách thức: các nền tảng muốn cộng tác cải thiện chất lượng dự đoán nhưng không thể chia sẻ dữ liệu trực tiếp do quy định bảo mật. Khó khăn chính là số lượng **overlapped users giữa các bên rất ít**, làm giảm hiệu quả federated learning hiện tại. Thêm vào đó, truyền tải thông tin mô hình trong training gây chi phí communication cao và rủi ro rò rỉ privacy. FedPDD đề xuất framework double distillation giải quyết cả hai vấn đề, hoạt động hiệu quả ngay cả khi overlapped users tối thiểu.

## 2. Phương pháp sử dụng

**Double Distillation Framework:**

1. **Explicit Knowledge Transfer**: Mô hình cục bộ học kiến thức tường minh từ bên thứ ba (partner) thông qua distillation trực tiếp
2. **Implicit Knowledge Transfer**: Học thêm kiến thức ngầm từ các dự đoán lịch sử, cho phép chia sẻ kiến thức ngay cả khi overlapped users rất ít

**Offline Training Scheme**: Thay vì truyền thông tin mô hình liên tục, sử dụng training ngoại tuyến — giảm chi phí communication và rủi ro rò rỉ privacy đáng kể, không cần đồng bộ liên tục.

**Differential Privacy Layer**: Lớp bảo vệ bổ sung cho thông tin được truyền tải, đảm bảo privacy guarantees formal.

## 3. Thành tựu đạt được

**HetRec-MovieLens** (α=0.1 overlapping):
- FedPDD Joint: 82.92% accuracy — vượt FTL **+3.98%**, FedKD **+1.27%**, PFML **+1.60%**

**Criteo** (α=0.1 overlapping):
- FedPDD Joint: 76.68% accuracy — vượt FTL **+2.78%**, FedKD **+1.21%**, Local DeepFM **+2.44-3.26%**

- Chấp nhận tại **IJCNN 2023**
- Hoạt động hiệu quả với overlapped users tối thiểu (α=0.1)
- Communication cost thấp hơn đáng kể so với online federated approaches

## 4. Hạn chế

- Hiệu suất giảm khi overlapped users quá ít — vẫn cần mức overlap tối thiểu nhất định
- Chỉ chứng minh cho **cộng tác 2 bên** (binary parties), mở rộng multi-party không được đề cập
- Giả định **không có overlapping features** trong cross-silo, hạn chế ứng dụng
- Offline training yêu cầu các bên phối hợp lịch trình training — không phải lúc nào cũng khả thi
- Với DP strict, accuracy giảm **~1.53%** — đánh đổi privacy-accuracy tồn tại
- Framework giả định các bên có data distributions tương đối tương thích
