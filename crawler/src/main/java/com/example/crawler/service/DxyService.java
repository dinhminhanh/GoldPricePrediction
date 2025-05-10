package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.DxyCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.ChromeDriverContext;

@Service
public class DxyService {
	public boolean crawlWithChrome() {
        AMyDriverContext context = new ChromeDriverContext();
        return new DxyCrawler(context).crawl();
    }
}


