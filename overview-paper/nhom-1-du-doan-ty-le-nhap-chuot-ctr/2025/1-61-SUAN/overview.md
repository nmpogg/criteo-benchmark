# Review Paper: Exploring Scaling Laws of CTR Model for Online Performance Improvement

**ArXiv ID:** [2508.15326](https://arxiv.org/abs/2508.15326)
**Năm:** 2025 (RecSys 2025)
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Bài paper này nghiên cứu scaling laws trong mô hình dự đoán CTR (Click-Through Rate), lấy cảm hứng từ các quy luật scaling trong Large Language Models. Tác giả nhận thấy rằng các mô hình CTR truyền thống thường không được thiết kế để khai thác lợi ích của việc tăng kích thước mô hình và dữ liệu huấn luyện một cách hiệu quả, khiến hiệu suất cải thiện không đều đặn.

Vấn đề chính là: khi bạn muốn triển khai mô hình CTR có hiệu suất cao, nó sẽ yêu cầu chi phí tính toán lớn, không phù hợp với hạn chế latency trong các hệ thống thực tế. Đó là kỳ vọng ngoài quá cao để có thể tối ưu hóa cả hai yêu cầu này cùng lúc.

Paper này giải quyết gap bằng cách: (1) xây dựng mô hình CTR có khả năng scale tốt với scaling laws rõ ràng, (2) sử dụng distillation để chuyển giao kiến thức từ mô hình lớn sang mô hình nhỏ gọn có thể triển khai trên production, (3) chứng minh rằng mô hình nhỏ gọn sau distillation có thể vượt trội hơn mô hình lớn ở cấp độ cao hơn.

## 2. Phương pháp sử dụng

SUAN (Stacked Unified Attention Network) là đóng góp chính của paper. Kiến trúc này dựa trên thành phần cốt lõi gọi là Unified Attention Block (UAB), hoạt động như một encoder cho chuỗi hành vi người dùng (behavior sequences).

**Đặc điểm chính của UAB:** Nó hợp nhất mô hình hóa tính năng tuần tự (sequential) và không tuần tự (non-sequential) thành một cơ chế chung. Thay vì xử lý các loại tính năng này riêng biệt, UAB cung cấp một cách thống nhất để khai thác mối quan hệ giữa chúng. Bằng cách xếp chồng nhiều UABs, tác giả có thể tạo ra các model grades khác nhau (từ nhỏ đến lớn), cho phép khám phá scaling laws toàn diện.

**Chiến lược triển khai LightSUAN:** Để giảm chi phí suy luận, paper giới thiệu LightSUAN sử dụng sparse self-attention (chỉ tính attention giữa các cặp vị trí quan trọng) và parallel inference strategies để tối ưu hóa tốc độ. Sau đó, tác giả áp dụng online distillation để chuyển giao kiến thức từ SUAN (teacher) sang LightSUAN (student), nhằm mục đích: LightSUAN cấp độ thấp sau distillation sẽ hoạt động như LightSUAN cấp độ cao hơn mà không có teacher.

## 3. Thành tựu đạt được

Kết quả thí nghiệm cho thấy SUAN tuân theo scaling laws rõ ràng trong ba bậc độ lớn (spanning three orders of magnitude) liên quan đến cả kích thước mô hình và kích thước dữ liệu huấn luyện. Điều này có nghĩa là hiệu suất cải thiện một cách có thể dự đoán khi bạn tăng tài nguyên.

**Kết quả triển khai trực tuyến (online deployment):** Đây là phần quan trọng nhất. Khi triển khai LightSUAN sau distillation, hệ thống đạt được:
- **CTR increase: 2.81%** - tăng tỷ lệ người dùng click vào các item được gợi ý
- **CPM increase: 1.69%** - tăng chi phí trung bình mỗi 1000 lần hiển thị, phản ánh giá trị cao hơn của quảng cáo được dự đoán chính xác

Điều quan trọng là những cải thiện này đạt được mà vẫn duy trì thời gian suy luận chấp nhận được (acceptable inference latency), cho phép triển khai thành công trên hệ thống production có yêu cầu latency khắt khe.

## 4. Hạn chế

**Chi phí tính toán huấn luyện:** Mặc dù LightSUAN hiệu quả khi suy luận, quá trình huấn luyện SUAN (teacher) với kích thước lớn cần chi phí tính toán đáng kể. Paper không thảo luận chi tiết về thời gian huấn luyện tuyệt đối hoặc chi phí GPU cần thiết.

**Generalization qua các domain khác nhau:** Kết quả được báo cáo dường như từ một hệ thống cụ thể (khả năng từ recommendation hoặc advertising platform). Không rõ liệu scaling laws và hiệu suất distillation này có nhất quán khi áp dụng cho các domain khác (ví dụ: e-commerce, social media feed) hay không.

**Thiếu phân tích chi tiết về sparse attention:** LightSUAN sử dụng sparse self-attention để giảm chi phí, nhưng paper không cung cấp chi tiết về cách chọn lựa cặp vị trí để tính attention. Liệu có mất mát thông tin quan trọng từ việc loại bỏ các attention connections? Đánh giá độ nhạy cảm (sensitivity analysis) về mức độ sparsity cũng không được trình bày.

**Giới hạn của distillation:** Mặc dù LightSUAN sau distillation vượt trội hơn SUAN cấp độ cao hơn, vẫn chưa rõ distillation này có hoạt động tốt khi gap kích thước giữa teacher và student quá lớn không.
