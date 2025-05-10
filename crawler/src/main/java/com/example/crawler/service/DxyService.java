package com.example.crawler.service;

import org.springframework.stereotype.Service;

import com.example.crawler.crawler.DxyCrawler;
import com.example.crawler.driver.AMyDriverContext;
import com.example.crawler.driver.EdgeDriverContext;

@Service
public class DxyService {
	public boolean crawlWithEdge() {
        AMyDriverContext context = new EdgeDriverContext();
        return new DxyCrawler(context).crawl();
    }
}


