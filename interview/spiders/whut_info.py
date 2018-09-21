# -*- coding : utf-8 -*-
import scrapy
from ..items import InterviewItem
from time import strftime, localtime,time
from scrapy.mail import MailSender
#from ..setting import SEC_PER_DAY
class WhutInfo(scrapy.Spider):
    name = 'whut' 
    allowed_domains = ['scc.whut.edu.cn']
    start_urls = [
        'http://scc.whut.edu.cn/infoList.shtml?tid=1001&searchForm=&pageNow=1'
    ]

    def __init__(self, major='材料', day = '1', email_to = '1745148491@qq.com', *args, **kwargs):

        super().__init__(*args, **kwargs)
        day = int(day)
        deadline = localtime(time() - day * 24 * 3600)
        #deadline.tm_mday -= day
        self.date = strftime("%Y-%m-%d", deadline)
        self.major = major
        self.email_to = email_to

    def parse(self, response):
        
    #    urls = response.css('div.col_con ul li a::attr(href)').extract()
    #    print('urls',urls)
        dates = response.xpath('//div[@class = "col_con"]/ul/li/span/text()').extract()
        datetime = []
        for date in dates:
            date = date[1:][:-1]
            datetime.append(date)
        #    date = date[:-1]
        last_date = datetime[len(datetime)-1]
        
        for url, date in zip(response.css('div.col_con ul li a::attr(href)').extract(), datetime):
            if date < self.date:
                continue
            yield response.follow(url, callback=self.parse_detail)
        if last_date < self.date:
            return 
        pages = response.css('div.page ')
        num = len(pages.css('a::text').extract())
    #    print('num : ', num)
        try:
            next_page_index = pages.css('a::text').extract().index('下一页')
        except ValueError:
            print('fail:',pages.css('a::text').extract(), num)
            return 
    #    print('next_page_index : ', next_page_index)
    #    print('num : ', num)
        url = pages.css('a::attr(href)').extract()[next_page_index]
    #    print('url', url)
        yield response.follow(url, callback=self.parse, dont_filter=True)
    
    def parse_detail(self, response):
    #    pass
    #    company = response.css('div.nr-tit::text').extract_first()
        departments = response.xpath('//ul[@class = "joblist"]/li/dl/dd/div[2]/text()').extract()
    #    print('company:', company)
    #    print('departments:',departments)
        index = self.index(self.major, departments)
        if index == -1: return
        item = InterviewItem()
        item['name'] = response.css('div.nr-tit::text').extract_first()
        item['date'] = response.css('div.nr_fb span:contains("时间")::text').extract_first()
        locations = response.xpath('//ul[@class="joblist"]/li/dl/dd/div[last()]/text()').extract()
        item['location'] = locations[index]
        item['major'] = response.xpath('//ul[@class="joblist"]/li/dl/dd/div[3]/text()').extract()[index]
        numbers = response.xpath('//ul[@class="joblist"]/li/dl/dd/div[4]/text()').extract()
        item['numbers'] = numbers[index]
        item['website'] = response.url
    #    print(item)
        yield item

    def index(self, item, lists):
        n = 0
        for ls in lists:
            if item in ls:
                return n
            n += 1
        
        return -1

    def closed(self, reason):
    #    print('email info')
        mailer = MailSender.from_settings(self.settings)
        fname =  'whut_info' + strftime('%Y-%m-%d', localtime()) + '.txt'
        body = ''
        with open(fname, 'r', encoding='utf-8') as f:
            for line in f:
                body += line
        
        #body = str(body,encoding='utf-8')
        if body == '': 
            print('email nothing')
            return 
        subject = u'scrapy interview info on ' + strftime('%Y-%m-%d', localtime())
        mailer.send(to = self.email_to, subject= subject, body = body.encode('utf-8'),charset='utf-8')