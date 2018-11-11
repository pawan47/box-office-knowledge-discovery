import scrapy
import json
import os
import sys
import time

movies_directory = "movies/"
links_directory = "links/"
if not os.path.exists(movies_directory):
    os.makedirs(movies_directory)

if not os.path.exists(links_directory):
    os.makedirs(links_directory)

linkfile = "links/imdbLinks.json"
links_dict = {}
try:
    with open(linkfile,'r') as f:
        links_dict = json.load(f)
except:
    print("unable to open links file, movieCrawler will not run")
    pass

links = []
for key in links_dict:
    links.append("https://www.imdb.com" + links_dict[key])

class movieCrawler(scrapy.Spider):
    name = "movieCrawler"
    allowed_domains = ['imdb.com']
    start_urls = links

    people_links = {}
    detail_fields = ["Taglines:", "Country:", "Language:", "Budget:", "Cumulative Worldwide Gross:", "Production Co:"]
    director_fields = ["Director:", "Writers:"]

    def parse(self,response):
        movie = {}
        self.people_links = {}
        movie["Title"] = ' '.join(response.xpath('//div[@class="title_wrapper"]/h1/text()').extract_first().split()).replace(':',"")
        movie["Film_rating"] = ' '.join(response.xpath('//div[@class="subtext"]/text()').extract_first().split())
        if response.xpath('//div[@class="subtext"]/time/text()').extract_first()!=None:
            movie["Duration"] = ' '.join(response.xpath('//div[@class="subtext"]/time/text()').extract_first().split())
        else:
            movie["Duration"] = "NA"
        movie["Genre"], movie["release_date"] = self.getGenreReleaseDate(response.xpath('//div[@class="subtext"]/a'))
        movie["Description"] = ' '.join(response.xpath('//div[@class="summary_text"]/text()').extract_first().split())
        if response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()!=None:
            movie["IMDB_rating"] = ' '.join(response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first().split())
        else:
            movie["IMDB_rating"] = "NA"
        movie["IMDB_rating_count"] = ' '.join(response.xpath('//span[@itemprop="ratingCount"]/text()').extract_first().split())
        movie["Storyline"] = self.getStoryline(response.xpath('//div[@id="titleStoryLine"]/div[1]/p'))
        directors = self.getDirectors(response.xpath('//div[@class="credit_summary_item"]'))
        movie['Cast'] = self.getCastList(response.xpath('//table[@class="cast_list"]/tr'))
        movie['Taglines'] = self.getTagline(response.xpath('//div[@class="txt-block"]'))
        details = self.getDetails(response.xpath('//div[@id="titleDetails"]'))

        for key in directors:
            movie[key] = directors[key]
        
        for key in details:
            movie[key] = details[key]

        with open(movies_directory+movie["Title"]+".json", 'w') as f:
            json.dump(movie, f)
        
        with open(links_directory+movie["Title"]+" people"+'.json', 'w') as f:
            json.dump(self.people_links, f)
        
        for anchor in response.xpath('//div[@class="rec-title"]'):
            url = "https://www.imdb.com" + anchor.xpath('./a/@href').extract_first()
            if url!=None or url!="":
                #time.sleep(0.1)
                yield response.follow(url, callback=self.parse)
        
    def getGenreReleaseDate(self,subtext):
        vals = []
        for text in subtext:
            vals.append(text.xpath('./text()').extract_first())
        release_date = ' '.join(vals[-1].split())
        genre = []
        for val in vals[:-1]:
            for element in val.split():
                genre.append(element)
        return genre, release_date
    
    def getDirectors(self,csis):
        directors = {}
        for csi in csis:
            field = csi.xpath('./h4/text()').extract_first()
            if field==None:
                continue
            field = ' '.join(csi.xpath('./h4/text()').extract_first().split())
            if field in self.director_fields:
                lst = []
                for val in csi.xpath('./a'):
                    person = ' '.join(val.xpath('./text()').extract_first().split())
                    if "credits" not in person and "credit" not in person:
                        lst.append(person)
                        self.people_links[person] = val.xpath('./@href').extract_first()
                directors[field] = lst
        return directors
    
    def getCastList(self,casts):
        cast_list = []
        for row in casts:
            link = row.xpath('./td[not(@*)]/a')
            people = link.xpath('./text()').extract_first()
            if people != None:
                people = ' '.join(people.split())
                if "credits" not in people and "credit" not in people:
                    cast_list.append(people)
                    self.people_links[people] = link.xpath('./@href').extract_first()
        return cast_list
    
    def getTagline(self,txts):
        for txt in txts:
            text = txt.xpath('./h4/text()').extract_first()
            if text==None:
                continue
            text = ' '.join(txt.xpath('./h4/text()').extract_first().split())
            if text == "Taglines:":
                return ' '.join(txt.xpath('./text()').extract()[1].split())
    
    def getDetails(self,titleDetails):
        details = {}
        for detail in titleDetails.xpath('./div[@class="txt-block"]'):
            text = detail.xpath('./h4/text()').extract_first()
            if text==None:
                continue
            text = ' '.join(detail.xpath('./h4/text()').extract_first().split())
            if text=="Country:":
                countryList = []
                for country in detail.xpath('./a'):
                    countryList.append(' '.join(country.xpath('./text()').extract_first().split()))
                details["Country"] = countryList
            if text=="Language:":
                languageList = []
                for language in detail.xpath('./a'):
                    languageList.append(' '.join(language.xpath('./text()').extract_first().split()))
                details["Language"] = languageList
            if text=="Budget:":
                details["Budget"] = ' '.join(detail.xpath('./text()').extract()[1].split())
            if text=="Cumulative Worldwide Gross:":
                details["Revenue"] = ' '.join(detail.xpath('./text()').extract()[1].split())
        return details

    def getStoryline(self,tsl):
        texts = tsl.xpath('./span/text()').extract()
        storyline = ""
        for text in texts:
            text = ' '.join(text.split()).replace(" (", "").replace(")","")
            storyline += text
        return storyline