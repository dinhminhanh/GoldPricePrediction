package crawler;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;

import driver.AMyDriverContext;

public class SPXHistoryCrawler extends AMyCrawler {

	private static final String URL = "https://vn.investing.com/indices/us-spx-500-historical-data";
	private static final String JSON_PATH = "src/data/spx500.json";

	public SPXHistoryCrawler(AMyDriverContext myDriver) {
		super(myDriver);
	}

	@Override
	public boolean crawl() {
		driver.get(URL);
		driver.manage().window().maximize();
		driver.manage().deleteAllCookies();
		driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
		
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
		startDate.sendKeys("01-01-2015");

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
				// Ghi tiếp vào file JSON
				appendToJsonFile(JSON_PATH, newEntry);
				System.out.println("JSON Created: " + newEntry);
			} catch (JSONException e) {
				System.out.println("JSON Error: " + e.getMessage());
			}
		}

		driver.quit();
		return true;
	}
	
	private void appendToJsonFile(String filePath, JSONObject newEntry) {
		JSONArray jsonArray = new JSONArray();

		// Đọc dữ liệu JSON cũ nếu có
		try {
			String content = new String(Files.readAllBytes(Paths.get(filePath)));
			if (!content.isEmpty()) {
				jsonArray = new JSONArray(content);
			}
		} catch (IOException | JSONException e) {
			System.out.println("File not found or invalid JSON, creating new file...");
		}

		// Thêm dữ liệu mới vào mảng
		jsonArray.put(newEntry);

		// Ghi lại dữ liệu vào file
		try (FileWriter file = new FileWriter(filePath)) {
			try {
				file.write(jsonArray.toString(4));
			} catch (JSONException e) {
				e.printStackTrace();
			} 
			file.flush();
			System.out.println("Data appended to JSON file.");
		} catch (IOException e) {
			System.out.println("Error writing to JSON file: " + e.getMessage());
		}
	}

}
