# Review Paper: MoPEQ: Mixture of Mixed Precision Quantized Experts

**ArXiv ID:** [2509.02512](https://arxiv.org/abs/2509.02512)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Giải quyết thách thức deployment cho LLM & vision models với MoE:
- Post-training quantization gán mức precision khác nhau cho từng expert
- Dựa trên độ nhạy cảm của expert

## 2. Phương pháp sử dụng

- Hessian trace approximation để phân tích độ nhạy expert
- Per-expert granularity với clustering các expert tương tự
- Mixed precision quantization ở 2, 3, 4-bit
- Đánh giá trên VLMEvalKit benchmarks

## 3. Thành tựu đạt được

- Độ chính xác cạnh tranh với baseline uniform-precision
- Cải thiện đáng kể memory footprint
- Chấp nhận bởi ICCV Bivision Workshop 2025

## 4. Hạn chế

- Post-training quantization, chỉ kiểm tra 2-4 bit precisions
- Giới hạn trên kiến trúc MoE cụ thể
- Khả năng tổng quát hóa có thể bị ảnh hưởng
