package com.example.crawler.driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class ChromeDriverContext extends AMyDriverContext {
	
	public ChromeDriverContext() {
		System.setProperty("webdriver.chrome.driver", "src\\main\\java\\com\\example\\crawler\\lib\\chromedriver.exe");
		driver = new ChromeDriver() ;
	}

	@Override
	public WebDriver getDriver() {
		return driver;
	}
		
}
