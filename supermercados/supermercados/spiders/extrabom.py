import scrapy

class ExtrabomSpider(scrapy.Spider):
    name = 'extrabom'
    start_urls = ['https://www.extrabom.com.br/']

    def parse(self, response):
        # Seleciona todos os produtos na página
        for product in response.css('a.carousel__box__dados'):
            # Extrai o nome do produto
            name = product.css('.item-name .name-produto::text').get().strip()
            # Extrai o preço do produto
            price = product.css('.item-por__val::text').get().strip().replace('R$', '').replace(',', '.').strip()
            
            yield {
                'name': name,
                'price': price,
            }
        
        # Se houver um link para a próxima página, siga-o
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)