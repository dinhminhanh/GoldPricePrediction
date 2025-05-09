package crawler;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import driver.AMyDriverContext;

public class DxyCrawler extends AMyCrawler {

	private static final String URL = "https://vn.investing.com/indices/usdollar";
	private static final String JSON_PATH = "src/data/dxy.json";

	public DxyCrawler(AMyDriverContext myDriver) {
		super(myDriver);
	}

	@Override
	public boolean crawl() {
		driver.get(URL);
		driver.manage().window().maximize();
		driver.manage().deleteAllCookies();
		driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
//		WebDriverWait wait = new WebDriverWait(driver, 50);
//		wait.until(ExpectedConditions
//				.presenceOfElementLocated(By.cssSelector("div[data-test='instrument-header-details']")));
//		try {
//			Thread.sleep(3000);
//		} catch (InterruptedException e) {
//			e.printStackTrace();
//		}
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

			// Ghi tiếp vào file JSON
			appendToJsonFile(JSON_PATH, newEntry);
			System.out.println("JSON Created: " + newEntry);
		} catch (JSONException e) {
			System.out.println("JSON Error: " + e.getMessage());
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
