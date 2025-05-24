#!/bin/sh

# Gọi đến API của Spring Boot
curl -X GET http://crawler:8080/api/crawl/gold &
curl -X GET http://crawler:8080/api/crawl/dxy &
curl -X GET http://crawler:8080/api/crawl/oil &
curl -X GET http://crawler:8080/api/crawl/spx &

wait
