package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.SPXHistoryCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class SPXHistoryService {
    public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new SPXHistoryCrawler(context).crawl();
    }
}
