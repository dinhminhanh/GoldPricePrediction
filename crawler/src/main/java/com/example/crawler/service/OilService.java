package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.OilCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.EdgeDriverContext;

@Service
public class OilService {
	public boolean crawlWithEdge() {
        AMyDriverContext context = new EdgeDriverContext();
        return new OilCrawler(context).crawl();
    }
}


