package application.crawl.crawler;


import java.io.FileWriter;
import java.io.IOException;

import org.json.JSONArray;
import org.openqa.selenium.WebDriver;

import application.crawl.driver.AMyDriverContext;

public abstract class AMyCrawler {
	
	protected WebDriver driver ;
	protected JSONArray jdata  ;
	
	public AMyCrawler(AMyDriverContext myDriver) {
		this.driver = myDriver.getDriver() ;
		this.jdata  = new JSONArray() ;
	}
	
	public void saveAsJsonFile(String path) {
		String jString = jdata.toString();
        try (FileWriter file = new FileWriter(path)) {
        	file.write(jString);
        	file.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}
	};
	
	public abstract boolean crawl();
	
}
