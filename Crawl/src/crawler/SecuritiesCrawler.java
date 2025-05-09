package crawler;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import driver.AMyDriverContext;

public class SecuritiesCrawler extends AMyCrawler {

	private static final String URL = "https://vn.investing.com/indices/usa-indices?include-major-indices=true";
	private static final String JSON_PATH = "src/data/securities.json";

	public SecuritiesCrawler(AMyDriverContext myDriver) {
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
		List<WebElement> rows = driver.findElements(By.cssSelector("tbody.datatable-v2_body__8TXQk tr"));
		
		for (WebElement row : rows) {
		    List<WebElement> cells = row.findElements(By.tagName("td"));
		    
		    WebElement indiceElement = cells.get(1).findElement(By.cssSelector("a[href*='/indices/']"));
	        String indice = indiceElement.getAttribute("title");

	        String last = cells.get(2).getText();
	        String high = cells.get(3).getText();
	        String low = cells.get(4).getText(); 
	        String change = cells.get(5).getText();
	        String percent = cells.get(6).getText(); 
	        
	        WebElement timeElement = cells.get(7).findElement(By.cssSelector("time"));
	        String time = timeElement.getAttribute("datetime");
	        
	        LocalDate today = LocalDate.now();
	        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
	        String dateOnly = today.format(formatter);
		    
		    try {
				JSONObject newEntry = new JSONObject();
				newEntry.put("indice", indice);
				newEntry.put("last", last);
				newEntry.put("high", high);
				newEntry.put("low", low);
				newEntry.put("change", change);
				newEntry.put("percent", percent);
				newEntry.put("date", dateOnly);
				newEntry.put("time", time);

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
