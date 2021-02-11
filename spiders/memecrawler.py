import scrapy
from testecrawler.items import TestecrawlerItem

PAGES = 1
PAGE_URL = 'https://www.ahnegao.com.br/'

class MemeCrawler(scrapy.Spider):
    name = 'ahnegao_meme_spider'
    start_urls = [PAGE_URL] + [str(PAGE_URL + 'pag/') + str(page_num) for page_num in range(2, 2 + PAGES)]
    
    
    def parse(self, response):
        # taking all the url of blog posts
        contents = response.css('div.post-content')
        for content in contents:
            url = content.css('.entry-title a::attr(href)').get()
            print(url)
            yield response.follow(url, callback = self.getContent)
            
    def getContent(self,response):
        # in each blog post take all images url
        item = TestecrawlerItem()
        urls = response.css('div.entry-content p img::attr(src)').extract()
        item['image_urls'] = []
        for url in urls:
            item['image_urls'].append(response.urljoin(url))
        yield item
