import scrapy
import re
import csv
import string
import logging

class CashBackSpider(scrapy.Spider):
    name = "cashback"

    def start_requests(self):
        urls = [
            'https://www.cashbackmonitor.com/cashback-comparison/1/'
        ]
        for c in string.lowercase:
            urls.append(urls[0][:-2] + c + '/')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = {}
        cash_back_cols = {'Ebates': 5, 'Mr. Rebates': 8, 'Top Cashback': 10}
        result['Stores'] = response.css('tr.cmb td:first-child a::text').extract()
        for name, col in cash_back_cols.items():
            result[name] = response.css('tr.cmb td:nth-child({})'.format(col)).extract() 
        #cleaning
        # len == 9 ==> '<td></td>'
        p = re.compile('<a.*>(.*)</a>')
        for key,cash_back_list in result.items():
            if key == 'Stores':
                continue
            result[key] = ['0' if len(entry) == 9 else p.findall(entry)[0] for entry in cash_back_list]
        n = len(result['Stores'])
        if not all(len(x) == n for x in result.values()):
            logging.error('values length mismatch')
        yield result
