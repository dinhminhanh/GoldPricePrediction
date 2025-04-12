package application.crawl.crawler;

import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import application.crawl.driver.AMyDriverContext;

public class TwitterCrawler extends AMyCrawler {
	
	private static final String     URL       = "https://twitter.com/login" ;
	private static final String     JSON_PATH = "tweet.json"  ;
	
	public TwitterCrawler (AMyDriverContext myDriver) {
		super(myDriver);
	}
		
	@Override
	public boolean crawl() {
		boolean check = true ;
		String query = "#nft";		
		try {
			driver.get(URL);
	        driver.manage().window().maximize();
	        driver.manage().deleteAllCookies();
	        driver.manage().timeouts().pageLoadTimeout(40, TimeUnit.SECONDS);
	        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
			driver.findElement(By.xpath("//input[@name='text']")).sendKeys("Doraemo29925335");
			driver.findElement(By.xpath("//span[contains(text(),'Next')]")).click();
			Thread.sleep(1000);
			driver.findElement(By.xpath("//input[@name='password']")).sendKeys("03102003");
			Thread.sleep(1000);
			driver.findElement(By.xpath("//span[contains(text(),'Log in')]")).click();
			Thread.sleep(3000);
			driver.findElement(By.xpath("//input[@aria-label='Search query']")).sendKeys(query);
			Thread.sleep(1000);
			driver.findElement(By.xpath("//input[@aria-label='Search query']")).sendKeys(Keys.ENTER);
			Thread.sleep(1000);
		

		WebDriverWait wait = new WebDriverWait(driver, 50);
		//ArrayList<TwitterModel> listTweets = new ArrayList<TwitterModel>();
		
        while (jdata.length() <= 5) {	
            JavascriptExecutor js = (JavascriptExecutor) driver;
            js.executeScript("window.scrollBy(0, 1000)");
            try {
				Thread.sleep(3000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
            wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("a[aria-label*='ago']")));
        	
        	//account
            WebElement usernameElement = driver.findElement(By.cssSelector("div[data-testid='User-Name'] > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > span:nth-child(1)"));
            String acount = usernameElement.getText();
            System.out.println("User: " + acount);
            
            //date
            WebElement dateElement = driver.findElement(By.cssSelector("div[data-testid='User-Name'] > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > a:nth-child(1) > time:nth-child(1)"));
            String  dateString = dateElement.getAttribute("datetime");
            System.out.println("Date: " + dateString) ;
            
            /// hashtag
            WebElement hashtagElement = driver.findElement(By.cssSelector("div[data-testid='tweetText']"));
            String[] words = hashtagElement.getText().split("\\s+");
            String hashtagString = new String();
            for (String word : words) {
                if (word.contains("#")) {
                	hashtagString += word ;
                }
            }
            System.out.println("Hashtag: " + hashtagString);
            
            // postUrl
            WebElement postUrlElement = driver.findElement(By.cssSelector("div[data-testid='User-Name'] > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > a:nth-child(1)"));
    		String postUrl = postUrlElement.getAttribute("href")  ;
    		System.out.println("Post URL: " + postUrl);
    		
    		
    		//imgUrl
    		WebElement imageElement = driver.findElement(By.cssSelector("div[data-testid='tweetPhoto'] > img:nth-child(2)"));
            String imageUrl = imageElement.getAttribute("src");
            System.out.println("Image: " + imageUrl);
            
            // Views
            WebElement viewsElement = driver.findElement(By.cssSelector("a[aria-label*='views"));
            String viewsString = viewsElement.getAttribute("aria-label");
            viewsString = viewsString.substring(0, viewsString.indexOf(" "));
            int views = Integer.parseInt(viewsString);
            System.out.println("Views: " + views);
            
            // Likes
            WebElement likesElement = driver.findElement(By.cssSelector("div[data-testid='like']"));
            String likesString = likesElement.getAttribute("aria-label");
            likesString = likesString.substring(0, likesString.indexOf(" "));
            int likes = Integer.parseInt(likesString);
            System.out.println("Likes: " + likes);
            
            JSONObject a = new JSONObject();
            a.put("acount", acount) ;
            a.put("date"  , dateString);
            a.put("hashtag",hashtagString);
            a.put("imageUrl", imageUrl) ;
            a.put("postlUrl", postUrl) ;
            a.put("views", views) ;
            a.put("likes", likes) ;
            jdata.put(a);
         }
	    	driver.quit();
	    	
	    	// Remove Duplicate
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
		 } catch (InterruptedException  e) {
			check = false ;
		}
		return check ;
	}
}

