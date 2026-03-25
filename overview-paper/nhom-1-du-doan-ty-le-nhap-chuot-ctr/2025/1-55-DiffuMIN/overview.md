# Review Paper: DiffuMIN: Modeling Long-term User Behaviors with Diffusion-driven Multi-interest Network for CTR Prediction

**ArXiv ID:** [2508.15311](https://arxiv.org/abs/2508.15311)
**Năm:** 2025
**Nhóm:** 1 - Dự đoán tỷ lệ nhấp chuột (CTR) — Kiến trúc mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện mô hình CTR bằng cách mô hóa nhiều lợi ích người dùng (multi-interest) từ lịch sử hành vi dài hạn:
- Các phương pháp 2-stage hiện tại mất thông tin quan trọng
- Không capture đầy đủ phổ tùy thích người dùng

## 2. Phương pháp sử dụng

- Target-Oriented Interest Extraction: Orthogonal decomposition target → interest channels
- Diffusion-Based Augmentation: Generative module tạo thêm interests theo contextual factors
- Contrastive Learning: Đảm bảo generated interests align với authentic user preferences

## 3. Thành tựu đạt được

- Vượt baseline trên 2 public datasets + 1 industrial dataset
- Online A/B testing: +1.52% CTR, +1.10% CPM
- Code publicly available on GitHub

## 4. Hạn chế

- Hiệu quả tính toán với large-scale behavioral data chưa rõ
- Độ phức tạp xử lý noise trong user sequences
- Không thảo luận chi tiết về computational costs
