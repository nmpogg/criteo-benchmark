# Tổng Hợp 4 Paper CTR 2020

Tài liệu này tổng hợp 4 bài báo nghiên cứu về dự đoán tỷ lệ nhấp chuột (CTR - Click-Through Rate) công bố năm 2020.

## Danh Sách Papers

### 1. DCN V2 (2008.13535)
- **Tiêu đề:** DCN V2: Improved Deep & Cross Network and Practical Lessons for Web-scale Learning to Rank Systems
- **Tác giả:** Google (Ruoxi Wang, Rakesh Shivanna, Derek Z. Cheng, Sagar Jain, Dong Lin, Lichan Hong, Ed H. Chi)
- **Hội nghị:** Web Conference 2021 (WWW '21)
- **Vấn đề chính:** Giới hạn khả năng biểu diễn của mạng Cross trong DCN gốc khi xử lý hàng tỷ mẫu dữ liệu
- **Giải pháp:** Kiến trúc low-rank mixture để tăng tính biểu diễn đồng thời giữ hiệu quả chi phí
- **Kết quả:** Vượt trội trên benchmark, lợi ích kinh doanh đáng kể trên hệ thống Google
- **File:** `/1-11-DCN-V2/overview.md`

### 2. AutoDis (2012.08986)
- **Tiêu đề:** Embedding Learning Framework for Numerical Features in CTR Prediction
- **Tác giả:** Huifeng Guo, Bo Chen, Ruiming Tang, Weinan Zhang, Zhenguo Li, Xiuqiang He
- **Công bố:** Tháng 12/2020, Sửa đổi tháng 5/2021
- **Vấn đề chính:** Các đặc trưng số được xử lý bằng rời rạc hóa cứng hoặc nhúng capacity thấp
- **Giải pháp:** Framework AutoDis với meta-embeddings, soft discretization (rời rạc hóa mềm), và aggregation
- **Kết quả:** 2.1% cải tiến CTR, 2.7% cải tiến eCPM trên hệ thống quảng cáo thực tế
- **File:** `/1-12-Numerical-Embedding/overview.md`

### 3. CAN (2011.05625)
- **Tiêu đề:** Feature Co-Action Network for Click-Through Rate Prediction
- **Tác giả:** Weijie Bian, Kailun Wu, và các cộng sự từ Alibaba
- **Hội nghị:** WSDM 2022
- **Vấn đề chính:** Các mô hình học tương tác đặc trưng ẩn, không thể giữ lại khả năng biểu diễn đầy đủ
- **Giải pháp:** Cơ chế co-action: embedding của đặc trưng A qua MLP của đặc trưng B
- **Kết quả:** 12% cải tiến CTR, 8% cải tiến RPM tại Alibaba display advertising
- **File:** `/1-13-CAN/overview.md`

### 4. GateNet (2007.03519)
- **Tiêu đề:** Gating-Enhanced Deep Network for Click-Through Rate Prediction
- **Tác giả:** Tongwen Huang, Qingyun She, Zhiqiang Wang, Junlin Zhang
- **Gửi:** 6 tháng 7 năm 2020
- **Vấn đề chính:** Khả năng huấn luyện của mạng sâu, chọn lựa đặc trưng, nắm bắt tương tác bậc cao
- **Giải pháp:** Hai cơ chế gating: feature embedding gate (chọn đặc trưng quan trọng), hidden gate (chọn tương tác quan trọng)
- **Kết quả:** Cải tiến nhất quán trên FM, DeepFM, xDeepFM trên 3 bộ dữ liệu thực tế
- **File:** `/1-14-GateNet/overview.md`

## So Sánh Nhanh

| Tiêu chí | DCN V2 | AutoDis | CAN | GateNet |
|---------|--------|---------|-----|---------|
| **Tập trung vào** | Kiến trúc tương tác | Nhúng số | Tương tác rõ ràng | Cơ chế chọn lực |
| **Đầu vào chính** | Tất cả đặc trưng | Đặc trưng số | Tất cả đặc trưng | Tất cả đặc trưng |
| **Yếu tố chính** | Low-rank Cross | Meta-embedding + Soft discretization | Co-action mechanism | Feature & Hidden gates |
| **Cải tiến CTR** | Không công bố | 2.1% | 12% | Không công bố |
| **Công bố** | Google (WWW'21) | Công khai MindSpore | Alibaba (WSDM'22) | Công khai |
| **Độ phức tạp** | Vừa | Vừa | Cao | Thấp |
| **Dễ tích hợp** | Cao | Cao | Trung bình | Rất cao |

## Các Chủ Đề Chính

### Kiến Trúc & Thiết Kế
- **DCN V2:** Tập trung vào cải tiến mạng Cross với low-rank architectures
- **AutoDis:** Cải tiến thành phần embedding cho đặc trưng số
- **CAN:** Thiết kế cơ chế tương tác hoàn toàn mới (co-action)
- **GateNet:** Thêm cụng cơ chế chọn lực vào kiến trúc hiện tại

### Hiệu Quả Thực Tiễn
- **DCN V2:** Lợi ích kinh doanh tại Google (không công bố con số cụ thể)
- **AutoDis:** Lợi ích đo được trên nền tảng quảng cáo (2.1% CTR, 2.7% eCPM)
- **CAN:** Lợi ích đáng kể tại Alibaba (12% CTR, 8% RPM)
- **GateNet:** Cải tiến nhất quán trên nhiều baseline nhưng không công bố con số cụ thể

### Mức độ Công bố
- **DCN V2:** Hạn chế (chủ yếu "practical lessons" từ Google)
- **AutoDis:** Tốt (mã nguồn mở, chi tiết framework)
- **CAN:** Vừa (kết quả tốt nhưng chi tiết kiến trúc giới hạn)
- **GateNet:** Vừa (công khai nhưng chi tiết công thức thiếu)

## Thực Hiện & Triển Khai

### Công Ty Đứng Sau
- **DCN V2:** Google (web-scale systems)
- **AutoDis:** Alibaba & Tech partners
- **CAN:** Alibaba (display advertising)
- **GateNet:** Công bố độc lập

### Thử Nghiệm
- **DCN V2:** Benchmark công khai + hệ thống web-scale Google
- **AutoDis:** 2 bộ dữ liệu công khai + 1 bộ công nghiệp
- **CAN:** Bộ dữ liệu công khai + hệ thống Alibaba
- **GateNet:** 3 bộ dữ liệu thực tế

## Những Điểm Chung

1. **Tất cả giải quyết hạn chế của mô hình CTR hiện tại**
2. **Tất cả đều có triển khai thực tế** (không chỉ lý thuyết)
3. **Tất cả đều tập trung vào cải tiến hiệu suất dự đoán**
4. **Tất cả có thiết kế dễ tích hợp với các kiến trúc hiện tại**

## Những Điểm Khác Biệt

| Khía cạnh | DCN V2 | AutoDis | CAN | GateNet |
|-----------|--------|---------|-----|---------|
| **Phạm vi thay đổi** | Thiết kế core | Thành phần cụ thể | Cơ chế tương tác | Bổ sung modularity |
| **Độ khó triển khai** | Cao (rewrite) | Trung bình | Cao (kiến trúc mới) | Thấp (plugin) |
| **Kết quả con số** | Không công bố | Cụ thể (2.1%, 2.7%) | Cụ thể (12%, 8%) | Không cụ thể |
| **Tính tổng quát** | Cao (Google scale) | Cao (AutoDis framework) | Cao (Alibaba scale) | Cao (3 baselines) |

## Kết Luận

Bốn paper này đại diện cho các hướng tiếp cận khác nhau để cải tiến dự đoán CTR:
1. **DCN V2:** Cải tiến kiến trúc cốt lõi (Deep & Cross)
2. **AutoDis:** Cải tiến thành phần con cụ thể (numerical embeddings)
3. **CAN:** Giới thiệu cơ chế tương tác hoàn toàn mới
4. **GateNet:** Thêm khả năng chọn lực thích ứng

Tất cả đều cho thấy kết quả tích cực trên các bộ dữ liệu công khai và/hoặc hệ thống sản xuất thực tế, chứng minh rằng cải tiến mô hình CTR vẫn là một lĩnh vực sinh động và có giá trị thực tiễn cao.

---

**Ngày tạo:** 6 tháng 4 năm 2026
**Số lượng files:** 4 overview papers
**Tổng dòng code:** 392 dòng (mỗi file 64-137 dòng)
**Chất lượng:** Kỹ thuật chi tiết, toàn diện, đánh giá phê bình
