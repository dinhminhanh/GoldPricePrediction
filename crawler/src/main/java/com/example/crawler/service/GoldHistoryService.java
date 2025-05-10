package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.GoldHistoryCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.EdgeDriverContext;

@Service
public class GoldHistoryService {
	public boolean crawlWithEdge() {
        AMyDriverContext context = new EdgeDriverContext();
        return new GoldHistoryCrawler(context).crawl();
    }
}


