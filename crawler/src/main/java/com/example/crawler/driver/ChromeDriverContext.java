package com.example.crawler.driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class ChromeDriverContext extends AMyDriverContext {
	
	public ChromeDriverContext() {
		ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless"); // Chạy không giao diện (headless)
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");

        driver = new ChromeDriver(options);
	}

	@Override
	public WebDriver getDriver() {
		return driver;
	}
		
}
