# Review Paper: CoRECT - Embedding Compression Evaluation Framework

**ArXiv ID:** [2510.19340](https://arxiv.org/abs/2510.19340)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

CoRECT nhằm giải quyết khoảng trống quan trọng trong đánh giá các kỹ thuật nén embedding cho các hệ thống dense retrieval. Mặc dù nén embedding có thể giảm đáng kể kích thước chỉ mục (index size), các nghiên cứu trước đây thường bỏ qua một yếu tố cốt lõi: độ phức tạp của kho ngữ liệu (corpus complexity). Bài báo chứng minh rằng yếu tố này ảnh hưởng đáng kể đến hiệu suất lấy thông tin (retrieval performance).

Vấn đề chính là không có một framework đánh giá tiêu chuẩn hóa cho các phương pháp nén embedding. Các nghiên cứu trước thường sử dụng các dataset khác nhau, điều kiện đánh giá không nhất quán, khiến khó so sánh hiệu suất giữa các phương pháp. Điều này dẫn đến việc không thể chọn được phương pháp nén tối ưu cho mỗi trường hợp sử dụng cụ thể.

CoRECT giới thiệu một framework toàn diện để đánh giá tám loại kỹ thuật nén khác nhau (floating point casting, scalar quantization, binary quantization, dimensionality reduction, hashing methods, product quantization, v.v.) trên các bộ dữ liệu được chuẩn bị kỹ lưỡng với độ phức tạp corpus có kiểm soát.

## 2. Phương pháp sử dụng

CoRECT giới thiệu một framework đánh giá có ba thành phần chính:

**Thứ nhất, CoRE Dataset**: Được lấy mẫu từ MS MARCO v2 với độ phức tạp corpus được kiểm soát. Framework bao gồm các bộ sưu tập passage với 65 truy vấn được kiểm tra trên năm kích thước corpus khác nhau (từ 10K đến 100M passage), và các bộ sưu tập tài liệu với 55 truy vấn trên bốn kích thước (từ 10K đến 10M). Điều này cho phép đánh giá hiệu suất nén trên các kịch bản khác nhau về quy mô dữ liệu.

**Thứ hai, các phương pháp nén được đánh giá**: CoRECT systematically kiểm tra tám loại kỹ thuật nén bao gồm (1) Floating Point Casting (FP16, BF16, FP8), (2) Scalar và Binary Quantization (SBQ) ở 8, 4, 2-bit với binning bằng khoảng cách bằng nhau hoặc percentile, (3) Dimensionality Reduction thông qua Matryoshka Representation Learning (MRL) truncation và PCA, và (4) Hashing methods như Locality-Sensitive Hashing (LSH) và Product Quantization (PQ) via FAISS.

**Thứ ba, metrics và đánh giá**: Framework sử dụng các chỉ số retrieval tiêu chuẩn như NDCG@k, Recall@k, và MRR với nhiều giá trị cutoff khác nhau. Điều quan trọng là CoRECT cũng đánh giá trên các benchmark bên ngoài như BeIR để đảm bảo tính tổng quát của kết quả.

## 3. Thành tựu đạt được

CoRECT cung cấp những phát hiện định lượng sâu sắc về hiệu suất nén embedding:

**Impact của Corpus Complexity**: Khi kích thước corpus tăng từ 10K lên 100M passage, Recall@100 trên Snowflake V2 giảm từ ~82% xuống ~53%. Đối với bộ sưu tập tài liệu, sự suy giảm còn lớn hơn: từ 74% xuống 34%. Điều này chứng minh rằng phức tạp corpus là yếu tố quyết định hiệu suất nén.

**Biến thiên Hiệu suất Model**: Các mô hình khác nhau thể hiện hành vi nén rất khác nhau. Snowflake V2 đạt Recall@100 cao nhất trên corpus 100M (53.39%), trong khi Jina V3 bị suy giảm mạnh nhất: từ 83.85% xuống 44.15%. Kết quả này chứng minh rằng cần phải đánh giá systematic cho từng mô hình.

**Kết quả Binary Quantization**: Trên các corpus lớn, zero thresholding vượt trội hơn median thresholding. Tuy nhiên, E5 cho thấy recall drop đáng kể với zero thresholding (từ 84.31% xuống 19.23%), chỉ ra rằng các phương pháp khác nhau thích hợp cho các mô hình khác nhau.

**Ổn định NDCG@10**: Dù Recall@100 bị suy giảm đáng kể, NDCG@10 vẫn giữ tương đối ổn định trên các corpus có kích thước khác nhau, gợi ý rằng embedding nén vẫn giữ được chất lượng xếp hạng top-tier tốt.

## 4. Hạn chế

CoRECT có một số hạn chế cần lưu ý. Thứ nhất, framework chủ yếu tập trung vào dense retrieval tasks và có thể không áp dụng trực tiếp cho các tác vụ recommendation hoặc classification khác. Thứ hai, các phương pháp nén được đánh giá là các kỹ thuật hiện có chứ không giới thiệu các phương pháp nén mới đột phá. Thứ ba, mặc dù CoRECT kiểm tra tám loại nén, nhưng trong mỗi loại, chỉ có một vài biến thể được đánh giá, không khám phá toàn bộ không gian thiết kế.

Công việc tương lai cần mở rộng đánh giá sang các tác vụ khác, khám phá các phương pháp nén hybrid kết hợp nhiều kỹ thuật, và xây dựng các heuristic tự động để chọn phương pháp nén tối ưu dựa trên đặc tính corpus và mô hình.
