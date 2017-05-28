import scrapy

from bs4 import BeautifulSoup
from apple.items import AppleItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AppleCrawler(CrawlSpider):
	name ='apple'
	start_urls = ['http://www.appledaily.com.tw/realtimenews/section/new/']
	rules = [
		Rule(LinkExtractor(allow=('/realtimenews/section/new/[1-2]$')),callback='parse_list', follow=True)
	]
	def parse_list(self,response):
		domains = "http://www.appledaily.com.tw"
		res = BeautifulSoup(response.body)
		for news in res.select('.rtddt'):
			#print news.select('h1')[0].text
			#print domains + news.select('a')[0]['href']
			yield scrapy.Request(domains + news.select('a')[0]['href'],self.parse_detail)
	def parse_detail(self,response):
		res = BeautifulSoup(response.body)
		appleitem = AppleItem()
		appleitem['title'] = res.select('#h1')[0].text
		appleitem['content'] = res.select('.trans')[0].text
		appleitem['time'] = res.select('.gggs time')[0].text
		return appleitem