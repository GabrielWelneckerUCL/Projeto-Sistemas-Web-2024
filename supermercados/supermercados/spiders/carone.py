import scrapy

class CaroneSpider(scrapy.Spider):
    name = 'carone'
    start_urls = [
        'https://www.carone.com.br/alimentos',
        'https://www.carone.com.br/limpeza',
        'https://www.carone.com.br/adega',
        'https://www.carone.com.br/bebidas',
        'https://www.carone.com.br/frios-e-laticinios',
        'https://www.carone.com.br/carnes',
        'https://www.carone.com.br/congelados',
        'https://www.carone.com.br/hortifruti',
        'https://www.carone.com.br/especial-natal',
        'https://www.carone.com.br/utilidades',
        'https://www.carone.com.br/temperos-e-especiarias',
        'https://www.carone.com.br/infantil---bebe',
        'https://www.carone.com.br/bem-estar',
        'https://www.carone.com.br/bomboniere-e-doces',
        'https://www.carone.com.br/padaria-e-rotisseria',
        'https://www.carone.com.br/pet-shop',
        'https://www.carone.com.br/produtos-etnicos',
        'https://www.carone.com.br/higiene-e-beleza',
        'https://www.carone.com.br/higiene-pessoal'
    ]

    def parse(self, response):
        # Coleta produtos da página da categoria
        for product in response.css('.box-item.showcase-shelf-alternative'):
            name = product.css('.product-name a::text').get().strip()
            price_element = product.css('price-wc::attr(value)').get()
            best_price = product.css('addtocart-alternative-wc::attr(best-price)').get()

            # Se o valor do price-wc não estiver disponível, use o best-price
            price = price_element if price_element else best_price if best_price else 'Preço não disponível'

            yield {
                'name': name,
                'price': price,
            }

        # Paginando se houver mais produtos na categoria
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)