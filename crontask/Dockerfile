FROM alpine:latest

RUN apk add --no-cache curl busybox-suid

COPY curl-task.sh /curl-task.sh
RUN chmod +x /curl-task.sh

# Tạo cronjob
RUN echo "*/5 * * * * /curl-task.sh" > /etc/crontabs/root

CMD ["crond", "-f"]
