package com.example.crawler.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.crawler.service.DxyHistoryService;
import com.example.crawler.service.DxyService;
import com.example.crawler.service.GoldHistoryService;
import com.example.crawler.service.GoldService;
import com.example.crawler.service.OilHistoryService;
import com.example.crawler.service.OilService;
import com.example.crawler.service.SPXHistoryService;

@RestController
@RequestMapping("/api/crawl")
public class CrawlerController {
    
    @Autowired
    private GoldService goldService;

    @GetMapping("/gold")
    public ResponseEntity<String> crawlGold() {
        boolean result = goldService.crawlWithChrome();
        if (result) {
            return ResponseEntity.ok("Crawl thành công!");
        } else {
            return ResponseEntity.status(500).body("Crawl thất bại!");
        }
    }
    
    @Autowired
    private GoldHistoryService goldHistoryService;

    @GetMapping("/gold-history")
    public ResponseEntity<String> crawlGoldHistory() {
        boolean result = goldHistoryService.crawlWithChrome();
        if (result) {
            return ResponseEntity.ok("Crawl thành công!");
        } else {
            return ResponseEntity.status(500).body("Crawl thất bại!");
        }
    }
    
    @Autowired
    private OilService oilService;

    @GetMapping("/oil")
    public ResponseEntity<String> crawlOil() {
        boolean result = oilService.crawlWithChrome();
        if (result) {
            return ResponseEntity.ok("Crawl thành công!");
        } else {
            return ResponseEntity.status(500).body("Crawl thất bại!");
        }
    }
    
    @Autowired
    private OilHistoryService oilHistoryService;

    @GetMapping("/oil-history")
    public ResponseEntity<String> crawlOilHistory() {
        boolean result = oilHistoryService.crawlWithChrome();
        if (result) {
            return ResponseEntity.ok("Crawl thành công!");
        } else {
            return ResponseEntity.status(500).body("Crawl thất bại!");
        }
    }
    
    @Autowired
    private DxyService dxyService;

    @GetMapping("/dxy")
    public ResponseEntity<String> crawlDxy() {
        boolean result = dxyService.crawlWithChrome();
        if (result) {
            return ResponseEntity.ok("Crawl thành công!");
        } else {
            return ResponseEntity.status(500).body("Crawl thất bại!");
        }
    }
    
    @Autowired
    private DxyHistoryService dxyHistoryService;

    @GetMapping("/dxy-history")
    public ResponseEntity<String> crawlDxyHistory() {
        boolean result = dxyHistoryService.crawlWithChrome();
        if (result) {
            return ResponseEntity.ok("Crawl thành công!");
        } else {
            return ResponseEntity.status(500).body("Crawl thất bại!");
        }
    }
    

    @Autowired
    private SPXHistoryService spxHistoryService;

    @GetMapping("/spx-history")
    public ResponseEntity<String> crawlSpxHistory() {
        boolean result = spxHistoryService.crawlWithChrome();
        if (result) {
            return ResponseEntity.ok("Crawl thành công!");
        } else {
            return ResponseEntity.status(500).body("Crawl thất bại!");
        }
    }
}
