#!/bin/sh

# Gọi đến API của Spring Boot
curl -X GET http://crawler-container:8080/api/crawl/gold-history &
curl -X GET http://crawler-container:8080/api/crawl/dxy-history &
curl -X GET http://crawler-container:8080/api/crawl/oil-history &

wait
