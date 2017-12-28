import scrapy

class ScrapeDefaultEndpoint(scrapy.Spider):
	name = 'scrapeDefaultEndpoint'

	start_urls = [
		'http://quotes.toscrape.com'
	]

	def parse(self,response):
		#SELECT ALL DIVS WITH CLASS 'quote'
		allQuotes = response.css('div.quote')

		for quote in allQuotes:
		#YIELD THE DATA AND STORE IT INTO A JSON FILE USING 'scrapy crawl scraperName -o quotes.json'
			yield{
			#EXTRACT THE FIRST LINE OF TEXT FROM THE SPAN WITH THE CLASS 'text'
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first()
			}

		#GO TO THE NEXT PAGE
		nextPage = response.css('li.next a::attr(href)').extract_first()
		if nextPage is not None:
			yield response.follow(nextPage, self.parse)

			



