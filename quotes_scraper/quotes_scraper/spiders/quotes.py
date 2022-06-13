import scrapy

# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page btn = //ul[@class="pager"]//li[@class="next"]/a/@href

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    # Definimos la configuración
    custom_settings = {
      'FEED_URI': 'quoes.json',
      'FEED_FORMAT': 'json',
      'CONCURRENT_REQUESTS': 24, # Max
      'MEMUSAGE_LIMIT_MB': 2048, # Memoria max
      'MEMUSAGE_NOTIFY_MAIK': ['m@pandalabs.mx'],
      'ROBOTSTXT_OBE': True, # ;)
      'USER_AGENT': 'PepitoMartinez',
      'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # Función para attach de quotes
    def parse_only_quotes(self, response, **kwargs):
      if kwargs:
        quotes = kwargs['quotes']
      quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

      next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
      if next_page_button_link:
        yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
      else:
        yield {
          'quotes': quotes
        }

    # Función para extraer title & top_tags
    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        
        # Pasando argumentos a nuestro spider
        top = getattr(self, 'top', None)
        if top:
          top = int(top)
          top_tags = top_tags[:top]

        yield {
          'title': title,
          'top_tags': top_tags
        }

        # pasamos a parse_only_quotes lo que ya traemos
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
          yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes':quotes})