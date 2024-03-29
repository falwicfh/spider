# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException


class SeleniumMiddlerware(object):
    """
    利用selenium，获取动态页面数据
    """
    def process_request(self, request, spider):

        # 判断请求是否来自第二个页面，只在第二个页面调用浏览器
        if spider.name == 'list_spider':
            # 实例化。selenium结合谷歌浏览器，
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            path = r'E:\chrome\chromedriver.exe'
            self.driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
           # self.driver = webdriver.Chrome('E:\chrome\chromedriver.exe') # 实在受不了每次测试都打开浏览器界面，所以换成无界面的了
            # 请求
            self.driver.get(request.url)
            time.sleep(5)
            self.driver.switch_to.frame("g_iframe")

            # 获取请求后得到的源码
            html = self.driver.page_source

            # 关闭浏览器
            self.driver.quit()

            # 构造一个请求的结果，将谷歌浏览器访问得到的结果构造成response，并返回给引擎
            response = scrapy.http.HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')
            return response
'''
class SeleniumMiddleware(object):
    def process_request(self,request,spider):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # 指定谷歌浏览器路径
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get(request.url)
        time.sleep(10)
        html = self.driver.page_source
        self.driver.quit()
        return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                            request=request)
'''

''''
class SeleniumMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def process_request(self, request, spider):
        if spider.name == 'list_spider':
            self.driver.get(request.url)
            time.sleep(13)
            self.driver.switch_to.frame("g-iframe")

            body = self.driver.page_source

            return HtmlResponse(self.driver.current_url,
                                body=body,
                                encoding='utf-8',
                                request=request)
'''

class Music163ListSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Music163ListDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
