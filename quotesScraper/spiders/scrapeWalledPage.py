import scrapy

class ScrapeWalledPage(scrapy.Spider):
	name = 'scrapeWalledPage'

	start_urls = [
		'http://quotes.toscrape.com/login'
	]

	def parse(self,response):
		#USE FORMREQUESTS TO LOGIN
		return scrapy.FormRequest.from_response(
			response,
			formdata = {'username':'admin','password':'admin'},
			callback = self.afterLogIn
			)		

	def afterLogIn(self, response):
		allQuotes = response.css('div.quote')

		for quote in allQuotes:
			yield{
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first()
			}

		#GO TO THE NEXT PAGE
		nextPage = response.css('li.next a::attr(href)').extract_first()
		if nextPage is not None:
			yield response.follow(nextPage, self.afterLogIn)



			



