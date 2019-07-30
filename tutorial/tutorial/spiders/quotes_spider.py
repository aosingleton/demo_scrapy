import scrapy


# creating base class with parse rules and starting websites
class QuotesSpider(scrapy.Spider):
    # naming our spider
    name = 'quotes'

    # special function that needs an iterable to work through
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # response of is a special TextResponse class that has additional methods
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes {}.html'.format(page)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file {}'.format(filename))


# creating shortcut class that has a start_urls element instead of a start requests
# class use parse callback automatically
# versiom of spider creates a raw file that we can use or store somewhere
class QuotesSpider2(scrapy.Spider):
    name = 'quotes2'
    start_urls = [
        'http://quotes.toscrape.com/page/3/',
        'http://quotes.toscrape.com/page/4/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)


# version of spider generates dictionary items
class QuotesSpider3(scrapy.Spider):
    name = "quotes3"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }


# class follows links recursively until a break condition is met
class QuotesSpider4(scrapy.Spider):
    name = "quotes4"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            """Above line equivalent to
                for url in urls:
                    yield scrapy.Request(url=url, callback=self.parse)
            """
        
        # shortcut for next logic is follow()
        # if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)