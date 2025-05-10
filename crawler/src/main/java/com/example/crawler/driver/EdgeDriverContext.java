package com.example.crawler.driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.edge.EdgeDriver;

public class EdgeDriverContext extends AMyDriverContext {
	
	public EdgeDriverContext() {
		System.setProperty("webdriver.edge.driver", "src\\main\\java\\com\\example\\crawler\\lib\\msedgedriver.exe");
		driver = new EdgeDriver() ;
	}

	@Override
	public WebDriver getDriver() {
		return driver;
	}
		
}
