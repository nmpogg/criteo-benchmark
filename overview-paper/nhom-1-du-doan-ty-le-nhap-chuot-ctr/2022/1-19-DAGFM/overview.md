# DAGFM — Directed Acyclic Graph Factorization Machines for CTR Prediction via Knowledge Distillation

**ArXiv:** [2211.11159](https://arxiv.org/abs/2211.11159)
**Năm:** 2022 | **Venue:** WSDM 2023
**Tác giả:** Zhen Tian, Ting Bai, Zibin Zhang, Zhiyuan Xu, Kangyi Lin, Ji-Rong Wen, Wayne Xin Zhao
**Code:** [github.com/RUCAIBox/DAGFM](https://github.com/rucaibox/dagfm)
**Nhóm:** 1 — Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết **mâu thuẫn giữa độ chính xác và chi phí tính toán** trong CTR prediction ở quy mô công nghiệp. Các mô hình CTR hiện đại (DCN, xDeepFM, AutoInt...) đạt hiệu suất cao nhờ học feature interaction bậc cao, nhưng chi phí tính toán quá lớn để triển khai real-time trên hệ thống hàng tỷ user (như WeChat). Paper đặt câu hỏi: **có thể nén kiến thức từ mô hình phức tạp (teacher) sang mô hình nhẹ (student) mà gần như không mất hiệu suất?**

**Bối cảnh:** Trong hệ thống recommender quy mô lớn, giai đoạn ranking cần mô hình vừa chính xác vừa nhanh. Các FM-based models (FmFM, FwFM) nhẹ nhưng kém chính xác; các deep models (DCN, xDeepFM) chính xác nhưng nặng. Chưa có framework nào kết hợp được cả hai.

---

## 2. Phương pháp sử dụng

### 2.1 DAGFM — Student Model

- Mô hình hóa feature interactions dưới dạng **Directed Acyclic Graph (DAG)**: mỗi **node** = 1 feature field, mỗi **cạnh có hướng** = 1 tương tác giữa 2 features với trọng số learnable
- Cấu trúc DAG cho phép biểu diễn **tương tác bậc tùy ý** (arbitrary-order) giữa các features một cách hiệu quả
- **Dynamic Programming (DP) algorithm:** chứng minh toán học rằng DAGFM có khả năng biểu diễn **bất kỳ explicit feature interaction nào** — đây là tính chất "approximately lossless" khi distill từ teacher

### 2.2 KD-DAGFM — Knowledge Distillation Framework

- **Teacher:** mô hình CTR phức tạp bất kỳ (DCN, xDeepFM, AutoInt, CIN...)
- **Student:** DAGFM nhẹ, học bắt chước output distribution của teacher
- **Quy trình 3 pha:**
  1. **Teacher training:** huấn luyện teacher model trên dataset
  2. **Distillation:** student DAGFM học từ soft labels của teacher (distillation loss)
  3. **Fine-tuning:** tinh chỉnh student trên ground truth labels

### 2.3 KD-DAGFM+ — Mở rộng cho implicit interactions

- KD-DAGFM gốc chỉ distill **explicit** feature interactions
- KD-DAGFM+ thêm khả năng distill cả **implicit** interactions (từ DNN components) của teacher
- Giúp transfer toàn diện kiến thức từ bất kỳ teacher phức tạp nào

---

## 3. Thành tựu đạt được

### Kết quả thực nghiệm

- **4 datasets:** Criteo, Avazu, MovieLens-1M, WeChat (industrial, hàng tỷ feature dimensions)
- **Hiệu suất gần lossless:** Độ lệch giữa DAGFM student và teacher chỉ ~10⁻³, nhỏ hơn **1000x** so với tiny MLP, **30x** so với FmFM, **300x** so với FwFM
- **Giảm 78.5% FLOPs:** KD-DAGFM đạt best performance với **<21.5% FLOPs** so với SOTA methods
- **Online A/B test trên WeChat:** Xác thực hiệu quả trên hệ thống production quy mô tỷ users
- Vượt trội cả offline (AUC/LogLoss) và online metrics

### Đóng góp chính

- Framework KD đầu tiên cho CTR prediction kết hợp DAG-based student
- Chứng minh lý thuyết (DP) về khả năng biểu diễn universal của DAGFM
- Mở ra hướng nghiên cứu "lightweight but powerful" cho CTR models

---

## 4. Hạn chế

- **Knowledge distillation không hoàn hảo:** Dù deviation rất nhỏ (10⁻³), student vẫn không reproduce 100% hành vi teacher, đặc biệt ở các edge cases hiếm gặp
- **Phụ thuộc chất lượng teacher:** Hiệu suất student bị giới hạn bởi teacher — teacher kém → student kém
- **Training overhead:** Quy trình 3 pha (teacher + distillation + fine-tuning) tốn thời gian training hơn so với train 1 model trực tiếp
- **Chỉ tập trung explicit interactions:** KD-DAGFM gốc bỏ qua implicit interactions; KD-DAGFM+ cải thiện nhưng cách distill implicit knowledge vẫn là open problem
- **DAG structure cố định:** Cấu trúc DAG được thiết kế sẵn, chưa tự động tìm cấu trúc tối ưu (AutoML cho DAG topology)
- **Generalization:** Chưa rõ liệu framework có hiệu quả khi teacher-student gap quá lớn (ví dụ teacher rất deep, student rất shallow)
