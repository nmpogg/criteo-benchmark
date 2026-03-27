# Review Paper: Modeling Long-term User Behaviors with Diffusion-driven Multi-interest Network for CTR Prediction

**ArXiv ID:** [2508.15311](https://arxiv.org/abs/2508.15311)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gích?

DiffuMIN tập trung vào bài toán modeling long-term user behaviors cho CTR prediction — cách hiểu các interest và preference của user dựa trên lịch sử hành động dài hạn. Motivation chính là current state-of-the-art two-stage models thường phải filter out significant information khi extract user interests, dẫn đến loss of important patterns.

Gap trong nghiên cứu hiện tại là traditional multi-interest extraction methods chỉ capture một subset của user interests do constraints của model architecture hoặc efficiency requirements. Điều này đặc biệt problematic khi user có diverse hoặc evolving interests qua thời gian. Các two-stage models thường tối ưu hóa cho efficiency nhưng sacrifice information completeness.

DiffuMIN nhận rằng để truly capture long-term user behaviors, cần phải: (1) extract multiple interest channels từ extensive behavior history, (2) generate new interest representations để augment user interest space, (3) ensure generated interests align với thực tế user preferences. Paper giải quyết vấn đề này bằng cách combine multi-interest modeling với generative techniques.

## 2. Phương pháp sử dụng

DiffuMIN đề xuất một framework gồm ba thành phần chính kết hợp orthogonal decomposition, diffusion modeling, và contrastive learning:

**1. Target-oriented Multi-interest Extraction:** Sử dụng orthogonal decomposition để identify multiple interest channels từ user behavior sequence. Orthogonal constraint đảm bảo các interest channels là independent và complementary — tránh redundancy. "Target-oriented" có nghĩa là extraction process được guided bởi target item, ensuring extracted interests relevant với current prediction task.

**2. Diffusion-driven Interest Generation:** Áp dụng diffusion module để generate additional interest representations dựa trên context. Diffusion process được guided bởi contextual information (e.g., temporal context, item categories) và extracted interest channels. Điều này cho phép model explore rộng hơn interest space và augment available interests.

**3. Contrastive Learning Alignment:** Sử dụng contrastive learning để ensure generated interests align tốt với genuine user preferences. Objective là maximize similarity giữa generated interests và true user behaviors, khi minimize similarity với random negatives. Điều này prevent diffusion process generate unrealistic interests.

**Kỹ thuật cốt lõi:** Technical novelty nằm ở việc kết hợp orthogonal decomposition (để disentangle interests), diffusion models (để generate diverse interests), và contrastive learning (để validate generation). Cách tiếp cận này cho phép model capture richer user interest space so với traditional attention-based extraction.

## 3. Thành tựu đạt được

**Offline Evaluation:** DiffuMIN được evaluated trên ba datasets — hai public datasets (không specified names trong abstract) và một industrial dataset. Paper reports superiority trên tất cả datasets, demonstrating effectiveness của approach.

**Online A/B Testing - CTR Improvement:** 1.52% CTR improvement trong production A/B testing. Đây là một significant improvement trong real-world e-commerce setting, nơi mà even 0.1% improvement có thể translate thành millions of additional clicks.

**Online A/B Testing - CPM Improvement:** 1.10% improvement trong Cost Per Mille (CPM), metric quan trọng cho advertising revenue. Điều này cho thấy không chỉ CTR được cải thiện, mà cả quality của traffic cũng improve, leading đến higher monetization.

**Reproducibility:** Source code được công bố trên GitHub, facilitating independent verification và community adoption.

## 4. Hạn chế

Một hạn chế chính là abstract không provide cụ thể offline metrics (AUC, LogLoss) hay baselines được compare với. Không rõ liệu 1.52% CTR improvement là so với những model nào, và liệu improvement này có consistent trên tất cả user segments hay không.

Về mặt computational complexity, sử dụng diffusion module kèm theo contrastive learning training có thể expensive. Paper không discuss training time, inference latency, hoặc memory overhead so với simpler approaches. Trong production settings, inference latency là critical — nếu model quá slow, nó không thể deploy.

Scalability của orthogonal decomposition đến very high-dimensional feature spaces chưa rõ. Khi feature dimensions tăng (e.g., millions of unique items hoặc behavioral features), cách orthogonal decomposition scale up như thế nào là question. Thêm vào đó, generalization của learned interest representations sang new users hoặc cold-start scenarios chưa addressed.

Paper cũng không clarify architectural details như: số interest channels sử dụng, diffusion steps, contrastive learning temperature settings, và cách parameters được tuned. Những details này important cho reproducibility và practitioners wanting apply approach.
