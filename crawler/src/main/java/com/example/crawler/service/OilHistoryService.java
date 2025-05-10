package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.OilHistoryCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class OilHistoryService {
	public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new OilHistoryCrawler(context).crawl();
    }
}


