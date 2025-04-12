package application.crawl.crawler;

import java.util.concurrent.TimeUnit;
import org.json.JSONObject;
import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import application.crawl.driver.AMyDriverContext;
import application.crawl.driver.EdgeDriverContext;

import java.io.IOException;
import java.util.HashSet;
import java.util.List;
import java.util.Set;


public class NfticallyBlogCrawler extends AMyCrawler {
	private static final String     URL       = "https://www.nftically.com/blog/" ;
	private static final String     JSON_PATH = "blog.json" ;
	
	public NfticallyBlogCrawler(AMyDriverContext myDriver) {
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
		 try {
        while (true) {	
            wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("div[id*='post-']")));
           
				Thread.sleep(3000);
			
            List<WebElement> blogsElements = driver.findElements(By.cssSelector("div[id*='post-']"));
            String checkDate = null;
            
        	for (WebElement n : blogsElements) {
        		
        		//Date
        		WebElement dateElement = n.findElement(By.cssSelector("div[class='blog-date'] > ul:nth-child(1) > li:nth-child(1)"));
        		checkDate = dateElement.getText();
        		if (!checkDate.contains("2023")) continue;
        		System.out.println("Date: " + checkDate);
        		
        		//author
        		WebElement authorElement = n.findElement(By.cssSelector("div[class='author'] > a:nth-child(1) > span:nth-child(2)"));
        		String author = authorElement.getText();
        		System.out.println("Author: " + author);
        		
        		//Tags
        		String classNameString = n.getAttribute("class");
                String[] words = classNameString.split("\\s+");
                String tagString = new String();
                for (String word : words) 
	                if (word.contains("tag")) {
	                	word = word.substring(4);
	                	tagString += word ;
	                }
                System.out.println("Tag: " + tagString);
                
                // Title
                WebElement titleElement = n.findElement(By.className("blog-title"));
        		String title  = titleElement.getText();
        		System.out.println("Title: " + title);
                
        		//BlogUrl
                WebElement blogURLElement = titleElement.findElement(By.cssSelector("a:nth-child(1)"));
                String  blogURL = blogURLElement.getAttribute("href");
        		System.out.println("URL: " + blogURL);
        		
        		//Describe
        		WebElement describElement = n.findElement(By.cssSelector("div[class='blog-info'] > p:nth-child(3)"));
        		String describe = describElement.getText();
        		System.out.println("Describe: " + describe);
        		
        		//Img
        		WebElement imgElement = n.findElement(By.cssSelector("div[class*='image'] > a:nth-child(1) > img:nth-child(1)"));
        		String img = imgElement.getAttribute("src");
        		System.out.println("Image: " + img);
        		
        		 JSONObject a = new JSONObject();
                 a.put("title", title) ;
                 a.put("tag"  , tagString);
                 a.put("describe",describe);
                 a.put("author", author) ;
                 a.put("date", checkDate) ;
                 a.put("blogImage", img) ;
                 a.put("blogURL", blogURL) ;
                
                 jdata.put(a);
        	}
        	if (!checkDate.contains("2023")) break;
        	
        		WebElement nextPageElement = driver.findElement(By.cssSelector("a[aria-label='Next Page']"));
            	driver.get(nextPageElement.getAttribute("href"));
        		Thread.sleep(3000);
        		
            }
             } catch (InterruptedException exception) {
				check = false ;
		   }  catch (NoSuchWindowException e) {
			   check = false ;   
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
		 
		 return check ;
	}
	
	
 }





