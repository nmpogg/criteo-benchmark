# criteo-benchmark

## Dataset

### 1. Criteo
Kaggle Criteo Dataset [Display Advertising Challenge](https://www.kaggle.com/c/criteo-display-ad-challenge)

#### Mô tả dữ liệu
- **train.txt** - Tập huấn luyện bao gồm một phần lưu lượng truy cập của Criteo trong khoảng thời gian 7 ngày. Mỗi dòng tương ứng với một quảng cáo hiển thị (display ad) được phục vụ bởi Criteo. Các mẫu dương (clicked) và âm (non-clicked) đều đã được lấy mẫu lại (subsampled) với các tỉ lệ khác nhau nhằm giảm kích thước của bộ dữ liệu. Các mẫu được sắp xếp theo thứ tự thời gian.
  
- **test.txt** - Tập kiểm tra được tạo theo cùng cách như tập huấn luyện nhưng áp dụng cho các sự kiện xảy ra vào ngày tiếp theo sau giai đoạn huấn luyện.

**Lưu ý:** Nhãn (label) của file `test.txt` không được công bố, vì vậy ở đây chúng ta sẽ chia ngẫu nhiên `train.csv` thành các tập **train**, **dev** và **test**.

#### Các trường dữ liệu
- **Label** - Biến mục tiêu cho biết quảng cáo có được nhấp chuột (clicked) hay không.  
- **I1-I13** - Tổng cộng 13 cột đặc trưng dạng số nguyên (integer features), chủ yếu là các đặc trưng dạng đếm (count features).  
- **C1-C26** - Tổng cộng 26 cột đặc trưng dạng phân loại (categorical features). Giá trị của các đặc trưng này đã được băm (hash) thành 32-bit nhằm mục đích ẩn danh dữ liệu.

Ý nghĩa của các đặc trưng này không được công bố.  
Khi một giá trị bị thiếu, trường dữ liệu sẽ để trống.