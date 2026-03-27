# Review Paper: From Scaling to Structured Expressivity: Rethinking Transformers for CTR Prediction

**ArXiv ID:** [2511.12081](https://arxiv.org/abs/2511.12081)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Paper này giải quyết một vấn đề cơ bản trong dự đoán CTR: mặc dù các mô hình deep learning có khả năng học phức tạp, nhưng khi tăng kích thước mô hình, cải tiến hiệu năng lại giảm dần (diminishing returns). Điều này trái ngược với các mô hình ngôn ngữ lớn (LLM) nơi mà việc scale-up mang lại những cải tiến đáng kể.

Tác giả xác định rằng nguyên nhân gốc rễ là "sự misalignment cấu trúc" (structural misalignment) trong cách Transformers được thiết kế. Transformers giả định rằng dữ liệu có tính chất compositionality tuần tự (sequential compositionality), nhưng dữ liệu CTR lại yêu cầu "suy luận tổ hợp trên các trường ngữ nghĩa có cardinality cao" (combinatorial reasoning over high-cardinality semantic fields).

Vấn đề này quan trọng vì nó ảnh hưởng trực tiếp đến hiệu quả compute trong các hệ thống quảng cáo lớn nhất thế giới, nơi CTR prediction là một phần quan trọng.

## 2. Phương pháp sử dụng

Để giải quyết vấn đề trên, tác giả giới thiệu **Field-Aware Transformer (FAT)**, một kiến trúc mới tích hợp các "field-based interaction priors" trực tiếp vào cơ chế attention của Transformers.

FAT sử dụng hai kỹ thuật cốt lõi:
- **Decomposed content alignment**: Tách riêng việc alignment nội dung dựa trên các field khác nhau
- **Cross-field modulation**: Modulation các interaction giữa các field để capture combinatorial patterns

Cách tiếp cận này đảm bảo rằng độ phức tạp mô hình tỷ lệ với số lượng fields (F) thay vì kích thước vocabulary (n). Điều này có ý nghĩa lý thuyết quan trọng: tác giả cung cấp "formal scaling law cho mô hình CTR" được grounded trong Rademacher complexity, cho phép ước lượng generalization bounds tighter hơn.

Kiến trúc FAT không chỉ là cải tiến empirical mà còn có nền tảng lý thuyết vững chắc về cách Transformers có thể được thiết kế để phù hợp với bản chất của CTR data.

## 3. Thành tựu đạt được

Kết quả thí nghiệm menunjukkan cải tiến đáng kể ở cả offline và online:

**Offline:** FAT đạt cải tiến tối đa **+0.51% AUC** so với các phương pháp state-of-the-art hiện tại. AUC là metric quan trọng trong CTR prediction vì nó đánh giá khả năng rank hóa của mô hình.

**Online (Production):** Khi deploy FAT trên hệ thống thực tế, hệ thống ghi nhận:
- **+2.33% CTR increase**: Tỷ lệ nhấp chuột tăng 2.33%
- **+0.66% RPM improvement**: Revenue Per Mille tăng 0.66%

Những con số này có ý nghĩa kinh tế lớn cho các công ty dựa trên quảng cáo. Đặc biệt, khác biệt giữa offline improvement (+0.51% AUC) và online improvement (+2.33% CTR) cho thấy giá trị thực sự của mô hình khi deploy vào sản phẩm.

## 4. Hạn chế

Mặc dù FAT có những kết quả ấn tượng, nhưng paper không rõ ràng thảo luận về những hạn chế:

**Về computational cost**: Paper không so sánh chi tiết latency và memory consumption của FAT so với Transformer baseline. Vì FAT có những phép toán cross-field modulation phức tạp, cần biết liệu overhead này có ảnh hưởng tới serving latency trong production.

**Về generalization**: Evaluation chủ yếu trên các dataset CTR benchmark (không nêu cụ thể dataset nào). Cần kiểm chứng xem FAT có generalize tốt trên các miền khác nhau (e-commerce, social media, search ads) hay chỉ tốt trên specific domains.

**Về scalability**: Mặc dù claim là scaling với F (số fields) thay vì vocabulary size, nhưng không có thí nghiệm về cách FAT scale khi F rất lớn (hàng nghìn fields trong các hệ thống thực tế).
