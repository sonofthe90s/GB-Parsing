import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        vacancy_links = response.css('div.3zucV._1fMKr.undefined._1NAsu a.attr::(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)
        print(response)
        pass

    def vacancy_parse(self, response: HtmlResponse):
        name_job = response.xpath('//h1/text()').extract_first()
        company_job = response.xpath('//span[@class="_3mfro _1hP6a _2JVkc _2VHxz"]/text() |'
                                     ' //h2[@class="_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI"]/text()').extract_first()
        city_job = response.xpath('//div[@class="f-test-address _3AQrx"]//text()').extract()
        salary_job_min = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()[1]
        salary_job_max = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()[3]
        currency_job = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()[5]
        link_job = response.url


        yield JobparserItem(name=name_job, company=company_job, city=city_job,
                            salary_min=salary_job_min, salary_max=salary_job_max,
                            currency=currency_job, link=link_job)
