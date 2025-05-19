# --- Build ứng dụng Spring Boot ---
FROM maven:3-eclipse-temurin-17 AS build
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

# --- Base image chứa sẵn Chrome và ChromeDriver ---
# FROM selenium/standalone-chrome:latest AS base
FROM seleniarm/standalone-chromium AS base

# --- Copy ứng dụng vào base image ---
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

# Mở cổng 8080
EXPOSE 8080

# --- Chạy ứng dụng Java ---
ENTRYPOINT ["java", "-jar", "app.jar"]
