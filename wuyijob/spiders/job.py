# -*- coding: utf-8 -*-
import scrapy
from wuyijob.items import jobitems
from scrapy_redis.spiders import RedisSpider
import hashlib

class JobSpider(RedisSpider):
    name = 'job'
    allowed_domains = ['51job.com']
    redis_key = 'job:start_urls'

    def parse(self,response):
        page= range(1,2001)
        location_num = 0
        location_id = []
        salary_list = []
        company_list = []

        while location_num<9:
            location_num += 1
            location_i = "0"+str(location_num)+"0000"
            location_id.append(location_i)
        location = 9

        while location <36:
            location+=1
            location_i = str(location)+"0000"
            location_id.append(location_i)

        salary_num = 0
        while salary_num < 9:
            salary_num += 1
            salary_l = "0" + str(salary_num)
            salary_list.append(salary_l)
        salary_n = 9

        while salary_n < 12:
            salary_n += 1
            salary_i = str(salary_n)
            salary_list.append(salary_i)
        company_num = 0

        while company_num < 9:
            company_num += 1
            company_n = "0" + str(company_num)
            company_list.append(company_n)
        company_n = 9

        while company_n < 11:
            company_n += 1
            company_nu = str(company_n)
            company_list.append(company_nu)

        for location in location_id:
            for salary in salary_list:
                for company in company_list:
                    for page in range(1,2001):
                        yield scrapy.Request('http://search.51job.com/list/'+str(location)+',000000,0000,00,9,'+str(scrapy)+',%2B,2,'+ str(page) +'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype='+str(company)+'&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=8&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',callback = self.parse_body)

    def parse_body(self, response):
        position_list = response.xpath('//div[@class="dw_table"]//div[@class="el"]')
        for positions in position_list:
            # print positions
            url= positions.xpath('.//p/span/a/@href').extract()[0]
            position = positions.xpath('.//p/span/a/@title').extract()[0]
            position_company = positions.xpath('.//span[@class="t2"]/a/@title').extract()[0]
            location = positions.xpath('.//span[@class="t3"]/text()').extract()[0]
            salary = positions.xpath('.//span[@class="t4"]/text()').extract()[0]
            time = positions.xpath('.//span[@class="t5"]/text()').extract()[0]

            info = {
                'url':url,
                'position': position,
                'position_company': position_company,
                'location': location,
                'salary': salary,
                'time': time,
            }
            yield scrapy.Request(url, callback=self.parse_detail, meta = info,priority=1)

    def parse_detail(self, response):
        detail_list = response.xpath('//div[@class="tBorderTop_box"]//div[@class="bmsg job_msg inbox"]/text()').extract()

        item = jobitems()
        item['job_duty'] = ','.join(detail_list)
        # print type(item['job_duty'])
        item['url'] = self.md5(response.meta['url'])
        item['position'] = response.meta['position']
        item['company'] = response.meta['position_company']
        item['location'] = response.meta['location']
        item['salary'] = response.meta['salary']
        item['time'] = response.meta['time']
        yield item

    def md5(self, data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()







