package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.OilCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class OilService {
	public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new OilCrawler(context).crawl();
    }
}


