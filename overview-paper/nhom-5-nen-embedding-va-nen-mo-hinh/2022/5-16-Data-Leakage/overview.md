# Review Paper: Data Leakage via Access Patterns of Sparse Features in Deep Learning-based Recommendation Systems

**ArXiv ID:** [2212.06264](https://arxiv.org/abs/2212.06264)
**Năm:** 2022
**Tác giả:** Hanieh Hashemi, Wenjie Xiong, Liu Ke, Kiwan Maeng, Murali Annavaram, G. Edward Suh, Hsien-Hsin S. Lee
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Sparse features chiếm 99% kích thước model trong DLRM nhưng ít được xem xét về mặt bảo mật. Các sparse features này encode hành vi người dùng (click history, interactions) và được dùng để index vào embedding tables. Paper nghiên cứu **lỗ hổng bảo mật** trong recommendation systems triển khai trên cloud: kẻ tấn công có thể **monitor access patterns** vào embedding tables để suy ra thông tin cá nhân người dùng.

**Motivation:** Ngay cả khi computation được bảo vệ (encrypted), access patterns tới bộ nhớ vẫn có thể bị quan sát trong untrusted cloud environments, tiết lộ hành vi browsing/mua hàng của user.

## 2. Phương pháp sử dụng

- **Threat Model:** Attacker ở untrusted cloud environment (co-located VM, malicious cloud admin)
- **Attack Vector:** Monitor/track embedding table access patterns trong recommendation queries — mỗi user query tạo ra unique access pattern tương ứng với sparse features của họ
- **Phân tích:** Đặc trưng hóa các loại attacks có thể exploit access pattern information để reconstruct user behavioral histories
- **Scope:** Tập trung vào sparse feature access (chiếm 99% model size) — vùng bị bỏ quên trong security research

## 3. Thành tựu đạt được

- **Lần đầu tiên** chỉ ra security risk nghiêm trọng từ embedding table access patterns trong cloud-hosted recommendation systems
- **Demonstration:** Chứng minh tính khả thi của attacks — kẻ tấn công có thể theo dõi access patterns để suy ra hành vi người dùng
- **Awareness:** Xác định critical security gap mà cộng đồng ML chưa quan tâm đúng mức
- **Impact rộng:** Áp dụng cho mọi recommendation system dùng embedding tables trên cloud

## 4. Hạn chế

- **Chỉ phân tích threat, chưa đề xuất defense:** Paper identify risks nhưng không propose cơ chế phòng chống cụ thể
- **Metrics hạn chế:** Không công bố detailed experimental results, attack success rates, false positive rates
- **Paper dạng abstract/short:** Full PDF không hoàn toàn accessible, thiếu comprehensive evaluation
- **Practical defense gap:** Chưa kiểm tra hiệu quả của các countermeasures tiềm năng (ORAM, differential privacy, etc.)
