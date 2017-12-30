import scrapy

class ScrapeSearch(scrapy.Spider):
	name = 'scrapeSearch'

	start_urls = ['http://quotes.toscrape.com/search.aspx']

#SINCE ASP.NET SITES USE __VIEWSTATES A LOT!!!

#1. For each author in the dropdown, pass the author name and __viewstate to /filter.aspx
#2. For each tag created after, pass tag and the new __viewstate to /filter.aspx
#3. Scrape resulting quote

	def parse(self,response):
		allAuthors = response.css('select#author option::attr(value)').extract()
		for author in allAuthors:
			viewstate = response.css('input#__VIEWSTATE::attr(value)').extract_first()
			yield scrapy.FormRequest(
					'http://quotes.toscrape.com/filter.aspx',
					formdata = {'author':author, '__VIEWSTATE':viewstate},
					callback = self.afterAuthor
				)	
			

	def afterAuthor(self, response):
		allTags = response.css('select#tag option::attr(value)').extract()
		for tag in allTags:
			author = response.css('select#author option[selected]::attr(value)').extract_first()
			viewstate = response.css('input#__VIEWSTATE::attr(value)').extract_first()
			yield scrapy.FormRequest(
					'http://quotes.toscrape.com/filter.aspx',
					formdata = {'author':author,'tag':tag, '__VIEWSTATE':viewstate },
					callback = self.afterSearch
				)	
			

	
		


	def afterSearch(self, response):
		#SELECT ALL DIVS WITH CLASS 'quote'
		allQuotes = response.css('div.quote')

		for quote in allQuotes:
			yield{
				'text': quote.css('span.content::text').extract_first(),
				'author': quote.css('span.author::text').extract_first(),
				'tag': quote.css('span.tag::text').extract_first()
			}


			



