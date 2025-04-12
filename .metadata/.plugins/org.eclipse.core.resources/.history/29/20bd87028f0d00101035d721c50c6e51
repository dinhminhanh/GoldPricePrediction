package application.crawl.crawler;

import java.awt.Checkbox;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import application.crawl.driver.AMyDriverContext;
import application.crawl.driver.EdgeDriverContext;
import application.database.model.OpenSeaModel;

public class OpenSeaCrawler extends AMyCrawler {
	
	private static final String     URL = "https://opensea.io/rankings/trending?sortBy=one_day_volume" ;
	private static final String     JSON_PATH = "collection.json" ;
	
	public OpenSeaCrawler(AMyDriverContext myDriver) {
		super(myDriver);
	}
	
	@Override
	public boolean crawl() {
		boolean check = true ;
		driver.get(URL);
        driver.manage().window().maximize();
        driver.manage().deleteAllCookies();
        driver.manage().timeouts().pageLoadTimeout(40, TimeUnit.SECONDS);
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
        WebDriverWait wait = new WebDriverWait(driver, 50);
    	wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("a[data-id='Item']")));
		JavascriptExecutor js = (JavascriptExecutor) driver;
		js.executeScript("window.scrollBy(0,500)");
		try {
			Thread.sleep(3000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		while (jdata.length() < 95) {
            wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("a[data-id='Item']")));
            try {
				Thread.sleep(3000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
            List<WebElement> nftElements = driver.findElements(By.cssSelector("a[data-id='Item']"));
            for (WebElement n : nftElements) {
            	try {
            		// GetRank
            		WebElement rankElement = n.findElement(By.cssSelector("div:nth-child(1) > div:nth-child(1)"));
                    int rank = Integer.parseInt(rankElement.getText());
                    System.out.println("Rank: " + rank);
                    
                    // GetName
                    WebElement collectionElement = n.findElement(By.cssSelector("div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)"));
                    String  name =  collectionElement.getText();
                    System.out.println("Collection: " + name);
                    
                    // GetVolume
                    WebElement volumeElement = n.findElement(By.cssSelector("div:nth-child(2) > div:nth-child(1) > span:nth-child(1) > div:nth-child(1)"));
          		    String     volume        =  volumeElement.getText();
                    System.out.println("Volume: " + volume);
                    
                    // GetPercentChange
                    WebElement percentElement = n.findElement(By.cssSelector("div:nth-child(3) > span:nth-child(1)"));
                    String percentChange = percentElement.getText();
                    System.out.println("%Change: " + percentChange);
                    
                    // GetFloorPrice
                    WebElement priceElement = n.findElement(By.cssSelector("div:nth-child(4) > div:nth-child(1) > span:nth-child(1)"));
                    String floorPrice = priceElement.getText();
                    System.out.println("Floor Price: " + floorPrice);
                    
                    // GetSales
                    WebElement salesElement = n.findElement(By.cssSelector("div:nth-child(5) > span:nth-child(1)"));
            		String saleString = salesElement.getText();
            		if (saleString.contains(","))      saleString = saleString.replace(",", "");
            		else if (saleString.contains("K")) saleString = saleString.replace("K", "");
            		int sales = Integer.parseInt(saleString) ;
            		System.out.println("Sales: " + sales);
            		
            		// Get DateTime
            		LocalDateTime currentDateTime = LocalDateTime.now();
        		    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        		    String dateString = currentDateTime.format(formatter);
        		    
        		    // Put to JsonObject
            		JSONObject a = new JSONObject();
                    a.put("rank", rank) ;
                    a.put("collection"  , name);
                    a.put("volume",volume);
                    a.put("percentChange", percentChange) ;
                    a.put("floorPrice", floorPrice) ;
                    a.put("sales", sales) ;
                    a.put("date", dateString) ;
        	        
                    jdata.put(a);
                    System.out.println(" ");
				 } catch (NumberFormatException e) {
					System.out.println("Error!");
			     }	
              }      
             js.executeScript("window.scrollBy(0,2200)");
		}
		driver.quit();
		
		Set<String> uniqueJsonStrings = new HashSet<>();
	    int length = jdata.length();
	
	    for (int i = 0; i < length; i++) {
	        JSONObject jsonObject = jdata.getJSONObject(i);
	        String jsonString = jsonObject.toString();
	
	        if (uniqueJsonStrings.contains(jsonString)) {
	            jdata.remove(i);
	            i--; 
	            length--; 
	        } 
	        else   uniqueJsonStrings.add(jsonString);
	     }	
	    
		saveAsJsonFile(JSON_PATH);
		return check ;
	}
	
}
