import scrapy
import json

class ScrapeInfiniteScroll(scrapy.Spider):
	name = 'scrapeinfinitescroll'

#INFINITE SCROLLING READS CONTENT FROM A JSON FILE. 
#HERE, THESE ARE SERVED FROM 'http://quotes.toscrape.com/api/quotes?page=n' FOR n>=1
	quote_url = 'http://quotes.toscrape.com/api/quotes?page='
	start_urls=[quote_url + "1"]

	def parse(self,response):
		data = json.loads(response.body)

		for item in data.get('quotes', []):
			yield{
			'text':item.get('text'),
			'author':item.get('author',{}).get('name')
			}
		if data['has_next']:
			nextPage = data['page']+1
			yield scrapy.Request(self.quote_url + str(nextPage))

		
			



