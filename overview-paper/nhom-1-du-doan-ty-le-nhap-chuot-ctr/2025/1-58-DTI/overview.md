# Review Paper: Towards An Efficient LLM Training Paradigm for CTR Prediction

**ArXiv ID:** [2503.01001](https://arxiv.org/abs/2503.01001)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Paper này tập trung vào một thách thức lớn khi sử dụng Large Language Models (LLM) cho CTR prediction: hiệu suất training rất kém. Khi huấn luyện LLM trên CTR tasks, phương pháp truyền thống yêu cầu xây dựng unique prompts cho mỗi user interaction, dẫn đến chi phí tính toán cực kỳ cao khi độ dài sequence tăng lên.

Vấn đề cụ thể nằm ở sliding-window paradigm hiện tại có độ phức tạp **O(mn²)**, nơi m là số user interactions và n là chiều dài hidden state. Điều này có nghĩa rằng chi phí training tăng lên theo hình quadratic khi số lượng tương tác tăng, khiến việc training LLM trên dữ liệu CTR thực tế trở nên prohibitively expensive.

Giải quyết vấn đề này rất quan trọng vì nó mở ra khả năng sử dụng LLM (với các khả năng understanding ngôn ngữ phong phú) cho CTR prediction, một task hiện đang phụ thuộc chủ yếu vào supervised learning models.

## 2. Phương pháp sử dụng

Tác giả giới thiệu **Dynamic Target Isolation (DTI)**, một phương pháp training fundamentally khác biệt so với sliding-window paradigm truyền thống.

DTI "structurally parallelizes the training of k target interactions" (nơi k >> 1), cho phép xử lý multiple targets đồng thời thay vì tuần tự. Phương pháp này khắc phục hai bottleneck cốt lõi:

**Hidden-state leakage**: Trong traditional approach, information từ một interaction bị "leak" vào prediction của interaction khác, làm giảm độc lập tính của các target. DTI isolates training targets để mỗi target được xử lý độc lập.

**Positional bias overfitting**: Sliding-window paradigm khiến mô hình dễ overfit trên positional patterns (tức là, mô hình học tính chất vị trí trong sequence thay vì semantic features thực sự). DTI breaks pattern này bằng cách dynamic assignment của targets.

Kỹ thuật cốt lõi của DTI là nó memungkinkan parallelization mà vẫn maintain tính coherence của training process, thay vì training sequentially.

## 3. Thành tựu đạt được

Kết quả DTI rất ấn tượng về mặt computational efficiency:

**Training time reduction: 92%** - Đây là con số chính. Training time giảm từ khoảng 70 giờ xuống còn 5 giờ trên benchmark datasets. Đây là improvement cực kỳ significant, cho phép các nhà nghiên cứu iterate nhanh hơn và experiment với các LLM khác nhau.

**Maintained prediction accuracy**: DTI không chỉ giảm training time, mà còn maintain hoặc thậm chí cải tiến prediction accuracy so với sliding-window baseline. Điều này chứng minh rằng parallelization không compromise chất lượng model.

**Computational complexity reduction**: Cải tiến từ O(mn²) sang một complexity thấp hơn (paper không nêu cụ thể, nhưng 92% time reduction ngụ ý significant asymptotic improvement).

Những kết quả này có tác động thực tế rất lớn: nó làm cho việc training LLM cho CTR prediction trở nên practical cho các tổ chức không có unlimited compute resources.

## 4. Hạn chế

Mặc dù DTI đạt được cải tiến training time remarkable, nhưng paper vẫn có những hạn chế:

**Về accuracy trade-offs**: Paper không cung cấp detailed breakdown về performance metrics (AUC, LogLoss, v.v.). Mặc dù claim "maintained accuracy", nhưng không có số liệu cụ thể so sánh, chỉ biết rằng accuracy được maintain.

**Về generalization**: DTI được evaluate trên "benchmark datasets" mà paper không specify rõ ràng. Cần kiểm chứng xem phương pháp này có generalize tốt trên các LLM architecture khác nhau (GPT-style, BERT-style, v.v.) hay chỉ tốt trên specific architectures.

**Về memory requirements**: Mặc dù training time giảm 92%, paper không discuss memory footprint. Parallelization thường yêu cầu more memory để hold multiple target computations simultaneously. Nếu memory requirement tăng lên, thì DTI có thể không practical cho các hệ thống với memory constraints.

**Về inference latency**: Không có thảo luận về latency serving. Mặc dù training được accelerate, nhưng inference performance của LLM-based CTR model có thể vẫn chậm so với lightweight models (biết rằng LLM typically slower than shallow networks).
