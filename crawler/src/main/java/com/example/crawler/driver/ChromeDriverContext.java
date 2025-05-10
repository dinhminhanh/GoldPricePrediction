package com.example.crawler.driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class ChromeDriverContext extends AMyDriverContext {
	
	public ChromeDriverContext() {
		System.setProperty("webdriver.chrome.driver", "/usr/local/bin/chromedriver");
		ChromeOptions options = new ChromeOptions();
		options.addArguments("--headless", "--no-sandbox", "--disable-dev-shm-usage");
		driver = new ChromeDriver(options);
	}

	@Override
	public WebDriver getDriver() {
		return driver;
	}
		
}
