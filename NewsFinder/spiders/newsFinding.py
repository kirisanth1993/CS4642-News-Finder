import scrapy
import json

class ItemSpider(scrapy.Spider):
    name = "news_spider"

    start_urls = ['https://www.news.lk/news']
    #To get the 10 page news
    for index in range(10,600,10):
        url = "https://www.news.lk/news?limit=10&start=" + str(index)
        start_urls.append(url)
        
    def parse(self, response):
        #add css path of single news
        links = response.css('div.catItemHeader h3 a ::attr(href)')
        
        for ref in links:
            yield response.follow(ref, self.parse_page)

    def parse_page(self, response):
        newsName = response.url.split("/")[-1]
        #create JSON
        pageFile = {}
        #take file name 
        pageFile["newsFileName"] =  newsName.strip()
        #take heading of the news
        pageFile["heading"] =  response.xpath('//*[@id="k2Container"]/div[1]/div[2]/h2/text()').extract_first().strip();
        #take date of news posted
        pageFile["newsDate"] =  response.xpath('//*[@id="k2Container"]/div[1]/div[1]/span/text()').extract_first().strip()
        #take month of news posted
        pageFile["newsMonth"] =  response.xpath('//*[@id="k2Container"]/div[1]/div[1]/span/span/text()').extract_first().strip()
        #take news's category
        pageFile["publishedCategory"] =  response.xpath('//*[@id="k2Container"]/div[1]/div[2]/div[1]/a/text()').extract_first().strip()
        #to get content
        pageFile["firstContent"] = ""
        Contents = response.xpath('//*[@id="k2Container"]/div[1]/div[3]/node()/text()')
        for firstContent in Contents:
            firstContent = firstContent.extract().strip()
            if(firstContent != "") :
                pageFile["firstContent"] += firstContent + "\n"
        
        pageFile["nextContent"] = "";
        secondContents = response.xpath('//*[@id="k2Container"]/div[1]/div[4]/node()/text()')
        for nextContent in secondContents:
            nextContent = nextContent.extract().strip()
            if(nextContent != "") :
                pageFile["nextContent"] += nextContent + "\n"
        
        pageFile["externalNewsLink"] =  response.xpath('//*[@id="k2Container"]/div[5]/a/text()').extract_first().strip()
        filename = 'outputs/file_%s.txt' % newsName
        
        #write the information in file
        with open(filename, 'w+') as f:
            json_data = json.dumps(pageFile)
            f.write((json_data))
        print('Saved file ' + filename)