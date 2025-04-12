package application.crawl.crawler;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import application.crawl.driver.AMyDriverContext;
import application.crawl.driver.EdgeDriverContext;

public class BinanceCrawler extends AMyCrawler {
	
	private static final String     URL = "https://www.binance.com/en/nft/ranking?tab=trend" ;
	private static final String     JSON_PATH = "src/dataJson/binance(1).json" ;
	
	public BinanceCrawler(AMyDriverContext myDriver) {
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
        driver.findElement(By.xpath("//button[contains(text(),'Accept')]")).click();
        try {
			Thread.sleep(3000);
			WebDriverWait wait = new WebDriverWait(driver, 50);
		    wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("a[href*='/collection/']")));
	        Thread.sleep(3000);    
        
        List<WebElement> elements = driver.findElements(By.cssSelector("a[href*='/collection/']"));
        
		for (WebElement n : elements) {
			
			// GetRank
			int rank ;
	    	WebElement rankElement = n.findElement(By.cssSelector("div:nth-child(1) > div:nth-child(1)"));
	    	if (rankElement.getText().equals("")) {
	        		WebElement rankSpecial = n.findElement(By.cssSelector("div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > img:nth-child(1)"));
	        		String     rankSrc     = rankSpecial.getAttribute("src");
	        		if      (rankSrc.contains("first_iii"))  rank = 1;
	        		else if (rankSrc.contains("second_iii")) rank = 2;
	        		else 									 rank = 3;
	    	}
	    	else    rank =  Integer.parseInt(rankElement.getText());
	        System.out.println("Rank: " + rank);
	        
	        // GetName
	        String collection ;
			WebElement collectionElement = n.findElement(By.cssSelector("div:nth-child(1) div:nth-child(3) div:nth-child(1) div:nth-child(1)"));
	        collection = collectionElement.getText();
	        System.out.println("Collection: " + collection);
	        
	        // GetVolume
	        String volume ;
		    WebElement volumeElement = n.findElement(By.cssSelector("div:nth-child(2) > div:nth-child(1) > div:nth-child(1)"));
		    volume = volumeElement.getText();
		    System.out.println("Volume: " + volume);
		    
		    // GetPercentChange
		    String percentChange ;
		    WebElement percentElement = n.findElement(By.cssSelector("div:nth-child(3) > div:nth-child(1) > div:nth-child(1)"));
		    percentChange = percentElement.getText();
		    System.out.println("%Change: " + percentChange);
		    
		    // GetFloorPrice
		    String floorPrice ;
		    WebElement priceElement =  n.findElement(By.cssSelector("div:nth-child(4) > div:nth-child(1) > div:nth-child(1)"));
		    floorPrice = priceElement.getText();
		    System.out.println("Floor Price: " + floorPrice );
		    
		    // GetOwners
		    int owners ;
	        WebElement ownersElement = n.findElement(By.cssSelector("div:nth-child(6)"));
	        String ownerString = ownersElement.getText();
	        if     (ownerString.contains(","))    owners = Integer.parseInt(ownerString.replace(",", ""));
	        else if(!ownerString.equals("--"))    owners = Integer.parseInt(ownerString); 
	        else  								  owners = 0;
	        System.out.println("Owners: " + owners);
	        
	        // GetItems
	        int items ;
		    WebElement itemsElement = n.findElement(By.cssSelector("div:nth-child(7)"));
		    String itemString = itemsElement.getText() ;
		    if     (itemsElement.getText().contains(","))  items = Integer.parseInt(itemString.replace(",", ""));
		    else if  (!itemString.equals("--"))            items = Integer.parseInt(itemString); 
		    else  										   items = 0;
		    System.out.println("Items: " + items);
		    
		    // GetDate
		    LocalDateTime currentDateTime = LocalDateTime.now();
		    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
		    String dateString = currentDateTime.format(formatter);
		    
		    JSONObject a = new JSONObject();
            a.put("rank", rank) ;
            a.put("collection"  , collection);
            a.put("volume",volume);
            a.put("percentChange", percentChange) ;
            a.put("floorPrice", floorPrice) ;
            a.put("owners", owners) ;
            a.put("items", items) ;
            a.put("date", dateString) ;
	        
            jdata.put(a);
	    }
		saveAsJsonFile(JSON_PATH);
		driver.quit();
        } catch (InterruptedException e) {
			check = false ;
		}    
        return check ;
	}
	
}