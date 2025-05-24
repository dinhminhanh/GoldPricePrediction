package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.SPXCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class SpxService {
	public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new SPXCrawler(context).crawl();
    }
}


