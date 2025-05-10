package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.DxyHistoryCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class DxyHistoryService {
	public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new DxyHistoryCrawler(context).crawl();
    }
}


