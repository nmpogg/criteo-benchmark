# Review Paper: GenCI — Generative Modeling of User Interest Shift via Cohort-based Intent Learning for CTR Prediction

**ArXiv:** [2601.18251](https://arxiv.org/abs/2601.18251) | **Năm:** 2026 | **Venue:** WWW 2026 Research Track
**Tác giả:** Kesha Ou, Zhen Tian, Wayne Xin Zhao, Hongyu Lu, Ji-Rong Wen

---

## 1. Paper này đang nghiên cứu gì?

Paper nghiên cứu bài toán **dự đoán CTR** với trọng tâm giải quyết hai vấn đề cốt lõi mà các mô hình discriminative truyền thống gặp phải:

- **Overfitting trên historical features:** Các mô hình discriminative hiện tại có xu hướng bám quá chặt vào các đặc trưng lịch sử chiếm ưu thế, dẫn đến không thể thích ứng khi sở thích người dùng thay đổi nhanh (interest shift). Khi user chuyển từ quan tâm thể thao sang công nghệ, mô hình vẫn tiếp tục đề xuất nội dung thể thao vì dữ liệu lịch sử chiếm đa số.
- **Mất tín hiệu ngữ cảnh do point-wise ranking:** Paradigm scoring từng candidate riêng lẻ (point-wise) loại bỏ contextual signals từ tập candidates đã recall, gây misalignment giữa long-term preferences và immediate intent của user. Ví dụ, trong một phiên tìm kiếm về laptop, việc score từng sản phẩm riêng lẻ mất đi thông tin về bối cảnh chung "user đang so sánh laptop".

**Ý tưởng chính:** Chuyển từ discriminative sang **generative paradigm** — thay vì phân loại click/no-click, mô hình sinh ra các "semantic interest cohorts" đại diện cho ý định hiện tại của user.

## 2. Phương pháp sử dụng

**GenCI Framework** — tiếp cận hai giai đoạn (two-stage):

**Giai đoạn 1 — Generative Interest Cohort Generation:**
- Sử dụng **generative model** với mục tiêu next-item prediction để sinh ra các **interest cohorts** — nhóm ngữ nghĩa đại diện cho immediate intent của user
- Cohorts này là candidate-agnostic (không phụ thuộc vào candidate cụ thể), cho phép capture ý định tổng quát của user tại thời điểm hiện tại
- Khác biệt với discriminative: thay vì dự đoán "user có click item X không?", mô hình sinh ra "user đang quan tâm đến nhóm chủ đề gì?"

**Giai đoạn 2 — Hierarchical Candidate-Aware Refinement:**
- Sử dụng **cross-attention mechanisms** để refine representations dựa trên candidate items cụ thể
- **Hierarchical candidate-aware network** tích hợp contextual signals từ tập recalled candidates
- Align ba thành phần: user history + immediate intent (từ cohorts) + target items

**Training:** End-to-end trên toàn bộ CTR prediction pipeline, đảm bảo hai giai đoạn tối ưu đồng thời.

## 3. Thành tựu đạt được

- **Kết quả thực nghiệm:** Hiệu quả trên 3 widely-used benchmark datasets, chứng minh generative paradigm khả thi cho CTR prediction
- **Alignment cải thiện:** Tạo alignment tốt hơn giữa user history, immediate intent, và target items so với discriminative baselines
- **Accepted tại WWW 2026 Research Track** — hội nghị hàng đầu về Web (acceptance rate thường ~20%)
- **Đóng góp lý thuyết:** Mở ra hướng nghiên cứu mới — áp dụng generative modeling vào CTR thay vì chỉ discriminative, tương tự xu hướng generative trong NLP/CV

## 4. Hạn chế

- **Thiếu metrics định lượng cụ thể** trong abstract: không báo cáo improvement percentage về AUC, LogLoss, hay các metrics chuẩn
- **Chi phí tính toán:** Generative approach (next-item prediction + cross-attention refinement) tiềm ẩn chi phí tính toán cao hơn đáng kể so với simple discriminative models, có thể ảnh hưởng đến khả năng triển khai real-time
- **Chưa có online A/B testing:** Chỉ đánh giá offline trên benchmark datasets, chưa chứng minh hiệu quả trong production environment
- **Scalability của cohort generation:** Khi số lượng interest categories lớn, việc sinh cohorts chính xác có thể khó khăn hơn
