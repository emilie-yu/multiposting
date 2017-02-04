import scrapy

class OffersSpider(scrapy.Spider):
    name = "offers"
    start_urls = ['http://jobs.careerpage.fr/career/multiposting-jobs-fr/',
                  'http://jobs.careerpage.fr/career/multiposting-internship-fr/',
                  ]

    def parse(self, response):
        # Scrape all offers found on the page by following links
        for offer_link in response.xpath('//table[@class="results"]//a/@href').extract():
            yield scrapy.Request(response.urljoin(offer_link),
                                 callback=self.parse_offer)

    def parse_offer(self, response):
        yield {
            'reference': response.url.split("/")[6],
            'title': response.xpath('//h2/text()'
            )
                    .extract_first(),
            'publication_date': response.xpath(
                '//li[./span[contains(text(), "Date")]]/span[@class="value"]/text()'
            )
                   .extract_first(),
            'country': response.xpath(
                'substring-after(//li[./span[contains(text(), "Loca")]]/span[@class="value"]/text(), ", ")'
            )
                   .extract_first(),
            'location_name': response.xpath(
                'substring-before(//li[./span[contains(text(), "Loca")]]/span[@class="value"]/text(), " (")'
            )
                   .extract_first(),
            'postal_code': response.xpath(
                'substring-before(substring-after(//li[./span[contains(text(), "Loca")]]/span[@class="value"]/text(), "("), ")")'
            )
                   .extract_first(),
            'education_level': response.xpath(
                '//li[./span[contains(text(), "Level") or contains(text(), "Niveau")]]/span[@class="value"]/text()'
            )
                   .extract_first(),
            'experience_level': response.xpath(
                '//li[./span[contains(text(), "Exp")]]/span[@class="value"]/text()'
            )
                   .extract_first(),
            'contract_type': response.xpath(
                '//li[./span[contains(text(), "contrat") or contains(text(),"Contract")]]/span[@class="value"]/text()'
            )
                   .extract_first(),
            'job_description': response.xpath(
                'normalize-space(//li[./h3[contains(text(), "Mission")]]/p)'
            )
                   .extract_first(),
            'profile_description': response.xpath(
                'normalize-space(//li[./h3[contains(text(), "Profil")]]/p)'
            )
                   .extract_first()
        }