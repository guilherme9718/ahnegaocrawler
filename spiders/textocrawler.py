import scrapy
import pandas as pd
import re

PAGES = 49
PAGE_URL = 'https://www.ahnegao.com.br/'
PAGE_ALT = 'https://www.ahnegao.com.br/t/coletanea-de-videos-bestas/'


class TextCrawler(scrapy.Spider):
    name = 'ahnegao_texto_spider'
    start_urls = [PAGE_ALT] + [str(PAGE_ALT + 'pag/') + str(page_num) for page_num in range(2, 2 + PAGES)]
    loop = 0
    page = 1
        
    def parse(self, response):
        # taking all the url of blog posts
        print('page = ', self.page)
        self.page += 1
        contents = response.css('div.post-content')
        for content in contents:
            title = content.css('h2.entry-title a::text').extract_first()
            title = ''.join(title).strip()
            url = content.css('.entry-title a::attr(href)').get()
            yield response.follow(url, callback = self.getContent)
            
    def getContent(self, response):
        # in each blog post take all text
        self.loop += 1
        
        title = response.css('h1.entry-title::text').extract_first()
        title = ''.join(title).strip()
        
        date = response.css('span.published::text').extract_first()
        date = ''.join(date).strip()
        
        text = response.css('div.entry-content p::text').extract()
        text = [x for x in text if x != u'\xa0']
        text_completed = ' \n'.join(text)
        
        data_dict = {'post':title, 'data':date, 'texto':text_completed}
        df = pd.DataFrame(data=data_dict, index=[0])
        if (self.loop == 1):
            h = True
            m = 'w'
        else:
            h = False
            m = 'a'
        yield df.to_csv(path_or_buf='textos_ahnegao.csv', index=False, header=h, mode=m)
