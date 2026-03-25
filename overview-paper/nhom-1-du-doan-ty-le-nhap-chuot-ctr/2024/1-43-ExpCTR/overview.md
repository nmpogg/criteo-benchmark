# Review Paper: ExpCTR: Explainable CTR Prediction via LLM Reasoning

**ArXiv ID:** [2412.02588](https://arxiv.org/abs/2412.02588)
**Năm:** 2024
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo giải quyết thiếu **tính minh bạch** trong hệ thống recommendation. Các phương pháp giải thích hiện tại là **post-hoc** — tạo giải thích sau khi model đã quyết định. Điều này gây 2 vấn đề: (1) độ tin cậy giải thích không đảm bảo vì giải thích có thể không phản ánh thực sự lý do model đưa ra quyết định, (2) cần nhiều nỗ lực thủ công xây dựng datasets giải thích. ExpCTR đề xuất tích hợp LLM-based explanation **trực tiếp vào quy trình prediction** thay vì post-hoc.

## 2. Phương pháp sử dụng

**ExpCTR** sử dụng 3 cơ chế:

- **LC Alignment Reward**: Đảm bảo giải thích phản ánh **user intent** — giải thích phải liên quan đến hành vi thực tế của user
- **IC Alignment Reward**: Đảm bảo **nhất quán với CTR models truyền thống** dựa trên ID — giải thích không mâu thuẫn với prediction
- **LoRA Training**: Điều chỉnh tham số LLM hiệu quả, không cần full fine-tuning
- Quy trình **3 giai đoạn iterative**: Tối ưu hóa chung accuracy và explainability
- Tránh yêu cầu datasets giải thích mở rộng — LLM tự generate explanations

## 3. Thành tựu đạt được

- Cải thiện đáng kể cả **prediction accuracy** lẫn **explainability** trên 3 real-world datasets
- Loại bỏ nhu cầu xây dựng explanation datasets mở rộng
- Tích hợp explanation vào prediction pipeline thay vì post-hoc

## 4. Hạn chế

- Thiếu con số định lượng (AUC, CTR lift, BLEU/ROUGE cho explanations)
- **Latency** và complexity của LLM reasoning ảnh hưởng CTR prediction real-time
- 3 iterative stages tốn computational resources đáng kể
- Chưa có **human evaluation** xác thực chất lượng và trustworthiness explanations
- Scalability trên domains ngoài e-commerce chưa kiểm tra
