package driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.edge.EdgeDriver;

public class EdgeDriverContext extends AMyDriverContext {
	
	public EdgeDriverContext() {
		System.setProperty("webdriver.edge.driver", "E:\\LINH\\Document\\BK\\20242\\DS\\Crawl\\src\\lib\\msedgedriver.exe");
		driver = new EdgeDriver() ;
	}

	@Override
	public WebDriver getDriver() {
		return driver;
	}
		
}
