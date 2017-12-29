import scrapy

#FOR RENDERING JS
from scrapy_splash import SplashRequest

class ScrapeJSContent(scrapy.Spider):
	name = 'scrapeJScontent'
	
	def start_requests(self):
		yield SplashRequest('http://quotes.toscrape.com/js')

	def parse(self,response):
		allQuotes = response.css('div.quote')

		for quote in allQuotes:
			yield{
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first()
			}

		#GO TO THE NEXT PAGE
		nextPage = response.css('li.next a::attr(href)').extract_first()
		if nextPage is not None:
			yield SplashRequest(response.urljoin(nextPage))		



