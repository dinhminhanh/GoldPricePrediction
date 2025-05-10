package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.GoldHistoryCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class GoldHistoryService {
	public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new GoldHistoryCrawler(context).crawl();
    }
}


