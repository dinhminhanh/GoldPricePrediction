import crawler.DxyCrawler;
import crawler.DxyHistoryCrawler;
import crawler.GoldCrawler;
import crawler.GoldHistoryCrawler;
import crawler.OilCrawler;
import crawler.OilHistoryCrawler;
import crawler.SPXHistoryCrawler;
import crawler.SecuritiesCrawler;
import driver.AMyDriverContext;
import driver.ChromeDriverContext;
import driver.EdgeDriverContext;

import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newFixedThreadPool(1);

//        Future<Boolean> goldFuture = executor.submit(() -> {
//            AMyDriverContext goldContext = new ChromeDriverContext();
//            return new GoldCrawler(goldContext).crawl();
//        });
//        
//        Future<Boolean> goldHistoryFuture = executor.submit(() -> {
//            AMyDriverContext goldHistoryContext = new EdgeDriverContext();
//            return new GoldHistoryCrawler(goldHistoryContext).crawl();
//        });
//
//        Future<Boolean> oilFuture = executor.submit(() -> {
//            AMyDriverContext oilContext = new ChromeDriverContext();
//            return new OilCrawler(oilContext).crawl();
//        });
        
//        Future<Boolean> oilHistoryFuture = executor.submit(() -> {
//            AMyDriverContext oilHistoryContext = new EdgeDriverContext();
//            return new OilHistoryCrawler(oilHistoryContext).crawl();
//        });
//        
//        Future<Boolean> dxyFuture = executor.submit(() -> {
//            AMyDriverContext dxyContext = new ChromeDriverContext();
//            return new DxyCrawler(dxyContext).crawl();
//        });
        
//        Future<Boolean> dxyHistoryFuture = executor.submit(() -> {
//            AMyDriverContext dxyHistoryContext = new EdgeDriverContext();
//            return new DxyHistoryCrawler(dxyHistoryContext).crawl();
//        });
//        
//        Future<Boolean> securitiesFuture = executor.submit(() -> {
//            AMyDriverContext securitiesContext = new ChromeDriverContext();
//            return new SecuritiesCrawler(securitiesContext).crawl();
//        });
        
        Future<Boolean> spxHistoryFuture = executor.submit(() -> {
            AMyDriverContext spxHistoryContext = new EdgeDriverContext();
            return new SPXHistoryCrawler(spxHistoryContext).crawl();
        });

        // Lấy kết quả
//        boolean goldResult = goldFuture.get();
//        boolean goldHistory = goldHistoryFuture.get();
//        boolean oilResult = oilFuture.get();
//        boolean oilHistory = oilHistoryFuture.get();
//        boolean dxyResult = dxyFuture.get();
//        boolean dxyHistory = dxyHistoryFuture.get();
//        boolean securitiesResult = securitiesFuture.get();
        boolean spxHistory = spxHistoryFuture.get();

        if (spxHistory) {
            System.out.println("Crawling completed successfully.");
        } else {
            System.out.println("Crawling encountered issues.");
        }

        executor.shutdown();
    }
}
