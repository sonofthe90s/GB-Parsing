import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract_first()
        vacancy_links = response.css('div.vacancy-serp div.vacancy-serp-item a.HH-LinkModifier::attr(href)').extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)
        yield response.follow(next_page, callback=self.parse)
        print(response)
        pass

    def vacancy_parse(self, response:HtmlResponse):
        name_job = response.xpath('//h1/text()').extract_first()
        company_job = response.xpath('//a[@data-qa="vacancy-company-name"]//text()').extract()
        city_job = response.xpath('//p[@data-qa="vacancy-view-location"]//text()').extract()[0]
        salary_job_min = response.css('p.vacancy-salary span::text').extract()[1]
        salary_job_max = response.css('p.vacancy-salary span::text').extract()[3]
        currency_job = response.css('p.vacancy-salary span::text').extract()[5]
        link_job = response.url

        yield JobparserItem(name=name_job, company=company_job, city=city_job,
                            salary_min=salary_job_min, salary_max=salary_job_max,
                            currency=currency_job, link=link_job)
