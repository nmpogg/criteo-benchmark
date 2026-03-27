# Review Paper: Two-Dimensional Sparse Parallelism for Large Scale Deep Learning Recommendation Model Training

**ArXiv ID:** [2508.03854](https://arxiv.org/abs/2508.03854)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình
**Tác giả:** Xin Zhang, Quanyu Zhu, Liangbei Xu, Zain Huda, và những người khác

---

## 1. Paper này đang nghiên cứu gì?

Bài báo tập trung vào vấn đề mở rộng huấn luyện Deep Learning Recommendation Models (DLRMs) với các bảng embedding lên tới hàng nghìn tỷ tham số. Bảng embedding chiếm 80-90% tổng số tham số và tài nguyên bộ nhớ trong các hệ thống khuyến nghị hiện tại. Khi phân phối trên hàng ngàn GPU, các phương pháp song parallel truyền thống gặp vấn đề nghiêm trọng: (1) chi phí giao tiếp all-to-all vượt 600ms ở 1000 GPUs, (2) dung lượng bộ nhớ hoạt động embedding tăng lên 15GB ở 1K GPUs, (3) không thể vượt quá ngưỡng bộ nhớ GPU hiện tại.

Vấn đề cơ bản nằm ở sự không hợp lý giữa chi phí giao tiếp tăng phi tuyến tính và hiệu suất huấn luyện. Các kỹ thuật hiện tại buộc phải tắt một số GPU vì không đủ bộ nhớ, giới hạn khả năng mở rộng tới 256-512 GPUs. Khoảng trống nghiên cứu: không có phương pháp song parallel nào chứng minh được khả năng mở rộng tới 4000+ GPU với tốc độ gần tuyến tính.

## 2. Phương pháp sử dụng

**Two-Dimensional Sparse Parallelism** chia T GPUs thành M nhóm với N=T/M GPUs mỗi nhóm. Thay vì phân phối bảng embedding trên tất cả T GPUs, mỗi nhóm duy trì một bản sao hoàn chỉnh với song parallel mô hình bên trong, còn song parallel dữ liệu áp dụng giữa các nhóm.

Hoạt động: (1) Mỗi nhóm xử lý phần dữ liệu batch độc lập với tra cứu embedding cục bộ, (2) Giao tiếp all-to-all chỉ trong nhóm (không trên tất cả GPUs), (3) Sau mỗi lần lặp, đồng bộ trọng số bảng embedding qua các nhóm. Chi phí giao tiếp được giảm từ 600ms xuống mức quản lý được.

**Momentum-Scaled Row-wise AdaGrad** giải quyết vấn đề hiệu suất. Khi song parallel thứ hai được áp dụng, momen bậc hai trong AdaGrad tích lũy nhanh hơn, gây "giảm tốc độ học không mong muốn". Giải pháp áp dụng hệ số tỷ lệ c: η/√(v/c + ε), trong đó c bằng M (số nhóm). Điều chỉnh này loại bỏ suy giảm entropy chuẩn hóa mà không mất hội tụ. Overhead bộ nhớ: S(M-1)/T GB trên mỗi GPU (bỏ qua được ở quy mô lớn).

## 3. Thành tựu đạt được

**Trên mô hình CTR (256 GPUs):**
- Tốc độ huấn luyện tăng gần gấp đôi: 1.53M → 2.66M QPS (M=4)
- Giảm bộ nhớ đỉnh ~20%: 72.4% → 54.74%
- Tỷ lệ mất cân bằng tải: 5.70 → 1.57

**Mô hình ExFM (1.7TB embedding):**

| GPU Count | Phương pháp cũ | 2D Sparse | Tỷ lệ mở rộng |
|-----------|----------------|-----------|--------------|
| 256       | 1.76×10⁵ QPS   | 1.76×10⁵  | —            |
| 512       | 3.37×10⁵       | 3.56×10⁵  | 100%         |
| 1024      | 5.61×10⁵ (OOM) | 6.76×10⁵  | 96%          |
| 2048      | OOM            | 1.34×10⁶  | 95%          |
| 4096      | OOM            | 2.53×10⁶  | 90%          |

**Kết quả chính:** Đạt tốc độ mở rộng gần tuyến tính lên 4000 GPUs (90% so với lý tưởng). Không suy giảm độ chính xác mô hình.

## 4. Hạn chế

- Yêu cầu nhân bản bảng embedding trên mỗi nhóm (overhead tăng với kích thước bảng >10TB)
- Hiệu suất mở rộng giảm dần ở quy mô siêu lớn (90% ở 4K GPU)
- Điều chỉnh tốc độ học yêu cầu biết kích thước nhóm M trước, không thích ứng động
- Chỉ đánh giá trên hai mô hình sản xuất (CTR, ExFM); tính chung chung chưa rõ
- Chỉ tập trung vào training, không xét suy luận phân tán
- Giả định mạng high-speed có sẵn (InfiniBand/RoCE)
