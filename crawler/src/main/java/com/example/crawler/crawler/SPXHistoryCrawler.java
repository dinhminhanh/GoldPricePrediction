package com.example.crawler.crawler;

import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;

import com.example.crawler.KafkaPublisher;
import com.example.crawler.driver.AMyDriverContext;

public class SPXHistoryCrawler extends AMyCrawler {

	private static final String URL = "https://vn.investing.com/indices/us-spx-500-historical-data";
	KafkaPublisher publisher = new KafkaPublisher("localhost:9092");
	String topic = "spx500-data";

	public SPXHistoryCrawler(AMyDriverContext myDriver) {
		super(myDriver);
	}

	@Override
	public boolean crawl() {
		driver.get(URL);
		driver.manage().window().setSize(new Dimension(1920, 1080));
		driver.manage().deleteAllCookies();
		try {
			driver.manage().timeouts().wait(5000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		};
		
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		Actions actions = new Actions(driver);
		actions.moveByOffset(10, 10).click().build().perform();
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		

		// Set date
		WebElement dateRangeInput = driver.findElement(By.cssSelector("div[class='relative flex items-center md:gap-6'] > div:nth-of-type(2)"));
		dateRangeInput.click();

		WebElement startDate = driver.findElement(By.cssSelector("div.NativeDateInputV2_root__uAIu0 > input"));;
		startDate.sendKeys("01-01-2025");

		WebElement applyButton = driver.findElement(By.cssSelector("g[filter='url(#back_right_svg__a)']"));
		applyButton.click();
		
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		JavascriptExecutor js = (JavascriptExecutor) driver;

		long scrollHeight = (Long) js.executeScript("return document.body.scrollHeight");

        // Cuộn từ từ
        long scrollPosition = 0;
        while (scrollPosition < scrollHeight) {
            // Cuộn xuống 500px
            js.executeScript("window.scrollBy(0, 500)");

            // Tăng vị trí cuộn
            scrollPosition += 500;

            // Đợi một chút trước khi cuộn tiếp (tùy chỉnh thời gian chờ)
            try {
                Thread.sleep(100); // 100ms
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
		
		List<WebElement> data = driver.findElements(By.cssSelector("tr.historical-data-v2_price__atUfP"));
		
		for (WebElement row : data) {
		    List<WebElement> cells = row.findElements(By.tagName("td"));
		    
		    String date = cells.get(0).getText();
	        String last = cells.get(1).getText();
	        String open = cells.get(2).getText();
	        String high = cells.get(3).getText();
	        String low = cells.get(4).getText(); 
	        String volume = cells.get(5).getText();
	        String percent = cells.get(6).getText(); 
		    
	        try {
	            JSONObject newEntry = new JSONObject();
	            newEntry.put("date", date);
	            newEntry.put("last", last);
	            newEntry.put("open", open);
	            newEntry.put("high", high);
	            newEntry.put("low", low);
	            newEntry.put("volume", volume);
	            newEntry.put("percent", percent);

	            // Gửi vào Kafka 
	            publisher.send(topic, date, newEntry.toString());
	            System.out.println("Sent to Kafka: " + newEntry);
	        } catch (JSONException e) {
	            System.out.println("JSON Error: " + e.getMessage());
	        }

		}
		publisher.close();
		driver.quit();
		return true;
	}
}
