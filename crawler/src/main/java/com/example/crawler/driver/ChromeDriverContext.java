package com.example.crawler.driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.io.*;
import java.nio.file.Files;

public class ChromeDriverContext extends AMyDriverContext {

    public ChromeDriverContext() {
        try {
            // Tải chromedriver từ resource và ghi ra file tạm
            InputStream input = getClass().getClassLoader().getResourceAsStream("bin/chromedriver");
            if (input == null) {
                throw new FileNotFoundException("Chromedriver not found in resources/bin/");
            }

            File tempDriver = Files.createTempFile("chromedriver", "").toFile();
            tempDriver.deleteOnExit();
            try (OutputStream out = new FileOutputStream(tempDriver)) {
                input.transferTo(out);
            }
            tempDriver.setExecutable(true);

            // Cấu hình system property để Selenium sử dụng chromedriver này
            System.setProperty("webdriver.chrome.driver", tempDriver.getAbsolutePath());

            // Cấu hình ChromeOptions
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--headless"); // Chạy không giao diện
            options.addArguments("--no-sandbox");
            options.addArguments("--disable-dev-shm-usage");

            driver = new ChromeDriver(options);
        } catch (IOException e) {
            throw new RuntimeException("Failed to initialize ChromeDriver", e);
        }
    }

    @Override
    public WebDriver getDriver() {
        return driver;
    }
}
