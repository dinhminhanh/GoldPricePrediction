package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.GoldCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class GoldService {
	public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new GoldCrawler(context).crawl();
    }
}


