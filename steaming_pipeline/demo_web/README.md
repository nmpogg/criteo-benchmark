# CTR Streaming Pipeline Live Demo

Dashboard này là demo động cho luồng upload Parquet và monitoring pipeline.

Chạy từ thư mục project root:

```bash
uvicorn demo_api.app:app --host 127.0.0.1 --port 9000
```

Mở:

```text
http://127.0.0.1:9000
```

Dashboard hiện làm được:

```text
Upload file parquet
Lưu file vào data/uploads
Inspect schema và số dòng
Tạo JSON event từ parquet
Gửi event vào Kafka topic ctr_events nếu Kafka đang chạy
Gắn run_id vào event_id để theo dõi output của đúng lần upload
Gửi Kafka có delay cấu hình được, mặc định 0.02 giây/event để giả lập realtime
Theo dõi PostgreSQL để biết Spark đã xử lý được bao nhiêu event
Hiển thị raw event, latest DB output, prediction, Kafka metadata, CTR chart và run log
```

Lưu ý:

```text
FastAPI không tự clean feature, không tự gọi model, không tự ghi PostgreSQL.
Spark Structured Streaming mới là nơi đọc Kafka, clean feature, gọi model,
ghi data/lake/processed_features và ghi PostgreSQL.
```
