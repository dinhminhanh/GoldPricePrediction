package com.example.crawler.crawler;

import org.json.JSONException;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebElement;

import com.example.crawler.KafkaPublisher;
import com.example.crawler.driver.AMyDriverContext;

public class GoldCrawler extends AMyCrawler {

	private static final String URL = "https://vn.investing.com/commodities/gold";
	KafkaPublisher publisher = new KafkaPublisher("localhost:9092");
	String topic = "gold-data";

	public GoldCrawler(AMyDriverContext myDriver) {
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
		
		WebElement n = driver.findElement(By.cssSelector("div[data-test='instrument-header-details']"));

		// GetPrice
		WebElement priceElement = n.findElement(By.cssSelector("div[data-test='instrument-price-last']"));
		String price = priceElement.getText();
		System.out.println("Price: " + price);

		// GetChange
		WebElement changeElement = n.findElement(By.cssSelector("span[data-test='instrument-price-change']"));
		String change = changeElement.getText();
		System.out.println("Change: " + change);

		// GetPercentChange
		WebElement percentElement = n
				.findElement(By.cssSelector("span[data-test='instrument-price-change-percent']"));
		String percentChange = percentElement.getText();
		System.out.println("%Change: " + percentChange);

		// Date
		WebElement timeElement = n.findElement(By.cssSelector("time[data-test='trading-time-label']"));
		String dateTime = timeElement.getAttribute("datetime");
		System.out.println("Datetime: " + dateTime);

		try {
			JSONObject newEntry = new JSONObject();
			newEntry.put("price", price);
			newEntry.put("change", change);
			newEntry.put("percentChange", percentChange);
			newEntry.put("datetime", dateTime);

			// Gửi vào Kafka 
            publisher.send(topic, dateTime, newEntry.toString());
            System.out.println("Sent to Kafka: " + newEntry);
        } catch (JSONException e) {
            System.out.println("JSON Error: " + e.getMessage());
        }

	    publisher.close();
		driver.quit();
		return true;
	}
}
