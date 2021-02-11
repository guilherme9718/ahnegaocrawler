import scrapy
import pandas as pd
import re
import os.path

PAGES = 6
PAGE_URL = 'https://www.ahnegao.com.br/'


class TextCrawler(scrapy.Spider):
    name = 'ahnegao_texto_spider'
    start_urls = [PAGE_URL] + [str(PAGE_URL + 'pag/') + str(page_num) for page_num in range(2, 2 + PAGES)]
    
    def parse(self, response):
        # taking all the url of blog posts
        contents = response.css('div.post-content')
        for content in contents:
            url = content.css('.entry-title a::attr(href)').get()
            print(url)
            yield response.follow(url, callback = self.getContent)
            
    def getContent(self,response):
        # in each blog post take all text
        title = response.css('h1.entry-title::text').extract_first()
        title = ''.join(title).strip()
        
        date = response.css('span.published::text').extract_first()
        date = ''.join(date).strip()
        
        text = response.css('div.entry-content p::text').extract()
        for string in text:
            string = string.replace('\n', '.')
            string = re.sub('\W+',' ',string).strip()
        text_completed = '. '.join(text)
        
        data_dict = {'post':title, 'data':date, 'texto':text_completed}
        df = pd.DataFrame(data=data_dict, index=[0])
        if os.path.isfile('textos_ahnegao.csv'):
            h = False
            m = 'a'
        else:
            h = True
            m = 'w'
        yield df.to_csv(path_or_buf='textos_ahnegao.csv', index=False, header=h, mode=m)
