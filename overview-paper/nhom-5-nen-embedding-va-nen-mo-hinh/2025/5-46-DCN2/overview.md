# Review Paper: DCN²: Interplay of Implicit Collision Weights and Explicit Cross Layers for Large-Scale Recommendation

**ArXiv ID:** [2506.21624](https://arxiv.org/abs/2506.21624)
**Năm:** 2025
**Nhóm:** 5 - Nén Embedding & Nén mô hình

---

## 1. Paper này đang nghiên cứu gì?

Cải thiện DCNv2 - kiến trúc phổ biến trong production:
- Giải quyết limitation về information loss & collision handling
- Tối ưu hóa cho large-scale recommendation

## 2. Phương pháp sử dụng

- Implicit collision weight management: learnable lookup-level weights
- Explicit cross-layer refinements: giảm information loss
- Custom layer: mô hình pairwise similarities (tương tự Field-aware FM)

## 3. Thành tựu đạt được

- Xử lý > 0.5 tỷ predictions/giây trong live system
- Outperform DCNv2 ở offline testing & A/B tests
- Superior performance trên 4 public benchmark datasets
- Hiệu quả tính toán tương đương DCNv2

## 4. Hạn chế

- Không rõ constraint so với các kiến trúc khác
- Giới hạn trên wide & deep / cross network paradigm
- Performance gains phụ thuộc vào specific applications
