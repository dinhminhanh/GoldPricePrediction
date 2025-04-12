package driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class ChromeDriverContext extends AMyDriverContext {
	
	public ChromeDriverContext() {
		System.setProperty("webdriver.chrome.driver", "E:\\LINH\\Document\\BK\\20242\\DS\\Crawl\\src\\lib\\chromedriver.exe");
		driver = new ChromeDriver() ;
	}

	@Override
	public WebDriver getDriver() {
		return driver;
	}
		
}
