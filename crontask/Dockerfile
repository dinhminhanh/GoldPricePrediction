FROM alpine:latest

RUN apk add --no-cache curl busybox-suid

COPY curl-task.sh /curl-task.sh
RUN chmod +x /curl-task.sh

# Thêm cron job chạy mỗi 5 phút
COPY crontab /etc/crontabs/root

CMD ["crond", "-f"]
