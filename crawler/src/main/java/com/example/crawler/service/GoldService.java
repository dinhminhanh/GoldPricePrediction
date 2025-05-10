package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.GoldCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.EdgeDriverContext;

@Service
public class GoldService {
	public boolean crawlWithEdge() {
        AMyDriverContext context = new EdgeDriverContext();
        return new GoldCrawler(context).crawl();
    }
}


