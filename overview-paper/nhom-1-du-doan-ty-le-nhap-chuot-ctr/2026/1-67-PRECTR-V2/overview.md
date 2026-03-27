# Review Paper: PRECTR-V2 — Unified Relevance-CTR Framework with Cross-User Preference Mining, Exposure Bias Correction, and LLM-Distilled Encoder

**ArXiv:** [2602.20676](https://arxiv.org/abs/2602.20676) | **Năm:** 2026
**Tác giả:** Shuzhi Cao, Rong Chen, Ailong He, Shuguang Han, Jufeng Chen

---

## 1. Paper này đang nghiên cứu gì?

Paper là **phiên bản nâng cấp của PRECTR** (paper #68), tiếp tục nghiên cứu bài toán **kết hợp search relevance matching và CTR prediction** trong hệ thống tìm kiếm. Cụ thể, PRECTR-V2 giải quyết 3 hạn chế còn tồn tại từ PRECTR:

- **Cold-start cho low-activity users:** Users mới hoặc ít tương tác thiếu dữ liệu hành vi, khiến việc personalize relevance gần như không thể. PRECTR gốc dựa trên behavioral data nên hoạt động kém với nhóm users này.
- **Exposure bias:** Dữ liệu training chỉ chứa items đã được hệ thống hiển thị (high-relevance exposure), tạo phân bố lệch (distribution mismatch) so với toàn bộ candidate space. Mô hình học từ dữ liệu thiên lệch → dự đoán thiên lệch.
- **Frozen BERT encoder:** PRECTR gốc sử dụng BERT pretrained nhưng đóng băng (frozen), không cho phép joint optimization giữa encoder và downstream tasks. Điều này giới hạn khả năng tinh chỉnh representations cho CTR cụ thể.

## 2. Phương pháp sử dụng

**PRECTR-V2 Framework** — 3 giải pháp cho 3 vấn đề:

**1. Cross-User Preference Mining (giải quyết cold-start):**
- Khai thác **global relevance preferences** từ toàn bộ users cho cùng một query
- Khi user A mới và search "iPhone 16", hệ thống tham khảo preferences của hàng nghìn users khác đã search query tương tự
- Cho phép cold-start personalization mà không cần behavioral data riêng

**2. Exposure Bias Correction (giải quyết distribution mismatch):**
- **Embedding noise injection:** Thêm nhiễu vào embedding space để tạo hard negative samples — items trông giống relevant nhưng thực tế không
- **Label reconstruction:** Gán lại labels cho noisy samples
- **Pairwise loss optimization:** Tối ưu relative ranking thay vì absolute scoring, giúp mô hình phân biệt tốt hơn giữa relevant/irrelevant items ở vùng ranh giới

**3. LLM-Distilled Encoder (giải quyết frozen encoder):**
- **Knowledge distillation từ LLM:** Pretrain một lightweight transformer encoder bằng cách "chưng cất" kiến thức từ LLM lớn
- **SFT trên text relevance classification:** Fine-tune encoder trên task phân loại relevance
- Thay thế hoàn toàn frozen BERT module, cho phép joint optimization end-to-end
- Lightweight hơn BERT nhưng capture semantic knowledge từ LLM

## 3. Thành tựu đạt được

- **Vượt qua paradigm Emb+MLP truyền thống:** Unified framework tích hợp relevance + CTR hiệu quả hơn pipeline tách rời
- **Giải quyết cold-start:** Cross-user mining cho phép phục vụ new/low-activity users mà PRECTR gốc không làm được
- **Lightweight inference:** LLM-distilled encoder nhẹ hơn BERT nhưng mạnh hơn nhờ kiến thức từ LLM
- **Systematic approach:** 3 vấn đề → 3 giải pháp tương ứng, dễ đánh giá đóng góp từng phần

## 4. Hạn chế

- **Thiếu numerical results** trong abstract — không báo cáo AUC, NDCG, hay bất kỳ metric định lượng nào
- **Chưa có online A/B testing** — paper submitted 02/2026, có thể chưa kịp triển khai production
- **Phụ thuộc vào LLM base:** Chất lượng distilled encoder phụ thuộc vào LLM được chọn để distill
- **Noise injection strategy:** Việc tạo hard negatives qua embedding noise có thể không đại diện cho real distribution mismatch
- **Chưa public benchmark:** Kết quả có thể chỉ trên proprietary datasets (tương tự PRECTR gốc)
