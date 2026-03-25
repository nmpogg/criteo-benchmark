# Review Paper: HoME: Hierarchy of Multi-Gate Experts for Multi-Task Learning at Kuaishou

**ArXiv ID:** [2408.05430](https://arxiv.org/abs/2408.05430)
**Năm:** 2024 | **Status:** Work in Progress | **Origin:** Kuaishou
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài báo phát hiện và giải quyết **3 anomalies nghiêm trọng** trong Mixture-of-Experts (MoE) cho multi-task learning, quan sát tại Kuaishou short-video platform:

- **Expert Collapse**: Phân phối output expert khác nhau đáng kể, **90%+ activations bằng không** khi dùng ReLU — hầu hết experts "chết"
- **Expert Degradation**: Shared experts dần trở thành **task-specific** thay vì phục vụ tất cả tasks — mất tính chia sẻ
- **Expert Underfitting**: Tasks có sparse data bỏ qua specific experts, **dựa hoàn toàn vào shared experts** — không học được task-specific patterns

## 2. Phương pháp sử dụng

**HoME (Hierarchy of Multi-Gate Experts):**

- **Kiến trúc phân cấp**: Tổ chức experts theo hierarchy thay vì flat — cho phép **phân bổ expert cân bằng hơn** giữa tasks
- **Multi-Gate mechanism đa cấp**: Gating ở nhiều levels đảm bảo experts không bị degrade thành task-specific, duy trì **shared property**
- **Load balancing**: Cơ chế cân bằng sử dụng expert giữa data-rich và data-sparse tasks
- Thiết kế đơn giản, hiệu quả, phù hợp xử lý **hàng chục concurrent prediction tasks** trên Kuaishou platform

## 3. Thành tựu đạt được

- Xác định và phân loại 3 anomalies quan trọng trong industrial MoE systems
- Giải pháp thực tế cho Kuaishou short-video recommendation — platform tỷ users
- Framework cân bằng expert utilization, duy trì efficiency ở quy mô lớn

## 4. Hạn chế

- **"Work in progress"** (tháng 8/2024) — **không có đánh giá thực nghiệm hoàn chỉnh**
- Không có số liệu so sánh với MoE methods hiện tại (MMoE, PLE, v.v.)
- Chi tiết cơ chế giải quyết expert collapse (load balancing, regularization) không nêu rõ
- Tác động lên các tasks khác nhau (data-rich vs data-sparse) không định lượng
- Phát triển chưa hoàn toàn — kết luận có thể thay đổi
