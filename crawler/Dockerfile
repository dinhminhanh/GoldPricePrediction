# --- Base image chứa sẵn Chrome và ChromeDriver ---
FROM selenium/standalone-chrome:latest AS base

# --- Build ứng dụng Spring Boot ---
FROM maven:3-eclipse-temurin-17 AS build
WORKDIR /app
COPY . .

# Copy chromedriver từ base image để nhúng vào resource
COPY --from=base /usr/bin/chromedriver ./src/main/resources/bin/chromedriver
RUN chmod +x ./src/main/resources/bin/chromedriver

RUN mvn clean package -DskipTests

# --- Copy ứng dụng vào base image và chạy ---
FROM base AS final
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
