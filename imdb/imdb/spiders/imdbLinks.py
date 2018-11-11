import scrapy
import json
import os

directory = "links/"
if not os.path.exists(directory):
    os.makedirs(directory)

class imdbLinks(scrapy.Spider):
    name = "imdbLinks"
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top']
    links = {}

    def parse(self,response):
        for row in response.xpath('//tbody[@class="lister-list"]/tr'):
            for movie in row.xpath('./td[@class="titleColumn"]/a'):
                movie_name = movie.xpath('./text()').extract_first()
                movie_link = movie.xpath('./@href').extract_first()
                self.links[movie_name] = movie_link
        with open(directory+self.name+'.json', 'w') as f:
            json.dump(self.links, f)