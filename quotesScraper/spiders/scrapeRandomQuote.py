import scrapy

class ScrapeRandomQuote(scrapy.Spider):
	name = 'scrapeRandomQuote'

	start_urls = [
		'http://quotes.toscrape.com/random'
	]

	#TO LIMIT NUMBER OF PAGE REQUESTS
	MAX_COUNT = 100
	count = 0

	def parse(self,response):
		allQuotes = response.css('div.quote')

		for quote in allQuotes:
			self.count = self.count + 1
			yield{
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first()
			}



		#REFRESH PAGE AND COLLECT MORE QUOTES
			#ADD 'dont_filter=True' FOR THE SPIDER TO RERUN ON THE SAME URL

		if(self.count<self.MAX_COUNT):
			yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True)

			



