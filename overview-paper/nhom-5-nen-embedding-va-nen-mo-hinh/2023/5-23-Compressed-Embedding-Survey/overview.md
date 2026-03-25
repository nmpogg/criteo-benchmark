# Review Paper: A Survey of Compressed Embedding Layers and Their Applications for Recommender Systems

**ArXiv ID:** [2306.13724](https://arxiv.org/abs/2306.13724)
**Năm:** 2023
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Các hệ thống khuyến nghị dựa trên neural network yêu cầu embedding layers khổng lồ với hàng tỷ tham số, tạo ra bottleneck bộ nhớ và tính toán nghiêm trọng. Trên các nền tảng e-commerce lớn, embedding tables cho hàng tỷ users/items chiếm phần lớn memory footprint. Tuy nhiên, chưa có survey nào tổng hợp toàn diện các kỹ thuật nén embedding trainable. Bài báo này lấp đầy khoảng trống đó bằng cách khảo sát và so sánh thực nghiệm 7 nhóm kỹ thuật nén embedding trên recommender systems.

## 2. Phương pháp sử dụng

Literature review kết hợp đo lường thực nghiệm trên 7 kỹ thuật nén embedding trainable:

- **Int4 Quantization**: Giảm float 32-bit xuống 4-bit integer kết hợp clustering, nén lý thuyết 8x
- **K-means Clustering**: Ánh xạ nhiều embedding vectors tới centroids, khai thác heavy-tailed feature distributions
- **Tensor-Train (TT) Decomposition**: Lưu trữ weights dưới dạng tensor-train format trong cả training và inference
- **Low-rank Decomposition**: Bao gồm thuật toán MEmCom và quotient-remainder tricks
- **Tensor-Ring Format**: Biến thể tensor-train với tradeoff nén/tính toán khác
- **Johnson-Lindenstrauss Projection**: Ánh xạ embeddings xuống dimensions thấp hơn, bảo toàn pairwise distances
- **Frobenius Layer**: Phương pháp decomposed embedding mới do tác giả đề xuất

Đánh giá thực nghiệm trên NCF (MovieLens-1M) và DLRM (Criteo-1TB) với A100/H100 GPUs.

## 3. Thành tựu đạt được

**DLRM trên Criteo-1TB (A100 GPU):**
- Model gốc: 0.8034 AUC, 14,407K samples/sec — Compressed: 0.8030 AUC, 11,812K samples/sec
- Training time: gốc 57 phút vs compressed 100 phút (3 epochs)

**Tỷ lệ nén đạt được:**
- Small variant: 15GB → 0.93GB (nén 16.2x)
- Large variant: 82GB → 0.58GB (nén 141x)
- Full variant: 421GB → 0.99GB (nén **425x**)

**MLPerf trên 8xH100:**
- Throughput: 3.7M → 147-151M samples/sec (cải thiện **40x**), accuracy loss negligible

## 4. Hạn chế

- Là survey tổng hợp, không đề xuất phương pháp hoàn toàn mới
- Overhead tính toán tăng đáng kể: training time tăng ~75% khi nén
- Không phân tích chi tiết tradeoff giữa compression ratio, accuracy, và computational cost cho từng kỹ thuật
- Phạm vi thực nghiệm hạn chế (chủ yếu DLRM + MovieLens), chưa rõ technique nào tốt nhất cho từng use case cụ thể
- Chi tiết loss metrics cho từng phương pháp không đầy đủ
