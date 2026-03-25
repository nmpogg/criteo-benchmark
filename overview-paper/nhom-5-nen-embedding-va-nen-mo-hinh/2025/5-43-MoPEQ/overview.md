# Review Paper: MoPEQ - Mixture of Mixed Precision Quantized Experts

**ArXiv ID:** [2509.02512](https://arxiv.org/abs/2509.02512)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

MoPEQ nhắm tới vấn đề triển khai các mô hình lớn với kiến trúc Mixture-of-Experts (MoE) trên các thiết bị có tài nguyên hạn chế. Các mô hình MoE, mặc dù hiệu quả về mặt tính toán, có yêu cầu bộ nhớ rất lớn vì phải lưu trữ trọng số của tất cả các experts, ngay cả khi chỉ một vài được kích hoạt trong mỗi forward pass.

Vấn đề kỹ thuật cốt lõi là làm thế nào để lượng tử hóa (quantize) các mô hình MoE mà không làm mất đáng kể accuracy. Các phương pháp lượng tử hóa truyền thống sử dụng độ chính xác (bit width) đồng nhất cho tất cả layer hoặc tất cả expert, nhưng điều này không tối ưu vì các expert có mức độ quan trọng khác nhau. Một số experts có thể lượng tử hóa ở 2-bit mà không ảnh hưởng hiệu suất, trong khi experts khác cần 4-bit để duy trì accuracy.

MoPEQ giải quyết vấn đề này bằng cách gán bit width tối ưu cho từng expert riêng lẻ, sử dụng Hessian trace approximation thay vì các phương pháp dựa trên activation frequency truyền thống.

## 2. Phương pháp sử dụng

MoPEQ giới thiệu ba thành phần kỹ thuật chính:

**Thứ nhất, Hessian Trace Approximation**: Thay vì tính toán Hessian matrix đầy đủ (phức tạp O(d³)), MoPEQ sử dụng Hutchinson algorithm để ước tính Hessian trace hiệu quả. Phương pháp này tính Frobenius norm proxy loss: ℒ=‖𝐖‖F=∑i,j Wij². Với mỗi sample, một vector ngẫu nhiên được lấy mẫu, gradient bậc một được tính toán, rồi Hessian-vector products được tính qua ∇𝐖(𝐠₁⊤𝐯) để tránh xây dựng Hessian rõ ràng. Trace cuối cùng được average qua nhiều samples. Tiếp cận "data-free" này cho phép đo độ nhạy (sensitivity) của expert mà không cần calibration dataset.

**Thứ hai, Expert Clustering Algorithm**: Sau khi tính toán importance của mỗi expert, MoPEQ sử dụng K-means clustering để gán bit width. Thuật toán phân chia các experts thành C clusters (C bằng số precision levels: 2, 3, hoặc 4 bits). Mỗi cluster's mean importance được tính toán, các clusters được sắp xếp theo importance giảm dần, và precision cao hơn được gán cho các clusters quan trọng hơn. Cách tiếp cận này tránh các splits cứng nhắc dựa trên phần trăm, cho phép các experts tương tự nhau nhận precision nhất quán.

**Thứ ba, SignRound Quantization Integration**: MoPEQ đánh giá lượng tử hóa trong khung AutoRound framework sử dụng SignRound quantization. Các baseline được so sánh bao gồm GPTQ (minimizing layer-wise reconstruction error sử dụng second-order information) và AWQ (activation-aware quantization). Không gian tìm kiếm thử nghiệm bao gồm precision 2-4 bits cho per-expert mixed-precision assignment.

## 3. Thành tựu đạt được

MoPEQ đạt được các kết quả quan trọng trong việc lượng tử hóa các mô hình MoE:

**Model-wise vs Layer-wise Precision**: Trên bốn mô hình Vision Language Model MoE (MolmoE-1B, DeepSeek-VL2 variants) và chín task VLMEvalKit, per-model precision allocation vượt trội so với per-layer approach: 63 trường hợp thắng so với 42.

**Tỷ lệ Nén**: Phương pháp sensitivity-based đạt khoảng 1.5× model size reduction while maintaining accuracy within 5% across bảy tasks. Trên MME perception task cụ thể, phương pháp đạt điểm 1338 so với uniform 4-bit baseline's 1300, với kích thước mô hình nhỏ hơn.

**Sử dụng Hiệu quả Bit**: Kết quả chứng minh rằng không phải tất cả experts đều cần precision cao. Bằng cách chỉ gán 3 hoặc 4 bits cho các experts quan trọng và 2 bits cho phần còn lại, hệ thống đạt được cân bằng tối ưu giữa độ nén và accuracy.

**Validation trên Mô hình Đa Kiến Trúc**: Phương pháp được đánh giá trên các mô hình khác nhau (vision, language, multimodal) với kiến trúc MoE khác nhau, chứng minh tính tổng quát của tiếp cận Hessian trace approximation.

## 4. Hạn chế

MoPEQ có một số hạn chế về phạm vi và khả năng tổng quát. Thứ nhất, bài báo chỉ đánh giá trên Vision Language Models (VLM) và không cung cấp kết quả cho Large Language Models (LLM) thuần túy hoặc các kiến trúc recommendation systems. Thứ hai, phương pháp sử dụng Hessian trace approximation có thể không phù hợp cho các activation functions rất phi tuyến, nơi Hessian có thể thay đổi nhanh.

Thứ ba, công việc không so sánh trực tiếp với các phương pháp per-expert quantization khác, chỉ so sánh với baselines layer-wise hoặc uniform-precision. Thứ tư, Hutchinson algorithm ước tính trace nhưng không xác định gradient sensitivity theo từng phần tử (element-wise), có thể bỏ lỡ một số fine-grained patterns.

Công việc tương lai cần mở rộng đánh giá sang LLM và recommendation models, khám phá hybrid approaches kết hợp Hessian sensitivity với activation-aware quantization, và phát triển các heuristic tự động để chọn số clusters tối ưu cho từng mô hình.
