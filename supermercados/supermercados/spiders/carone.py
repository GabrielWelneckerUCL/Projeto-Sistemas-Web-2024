import scrapy
import re

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
            brand = product.css('.product-brand::text').get().strip()  # Extraindo a marca
            name = product.css('.product-name a::text').get().strip()  # Extraindo o nome do produto
            
            # Capturando o HTML do produto como texto
            product_html = product.get()

            # Usando regex para encontrar preços nos comentários
            old_price_match = re.search(r'<!--\s*<span class="old-price">\s*(R\$ [\d,\.]+)\s*</span>', product_html)
            best_price_match = re.search(r'<!--\s*<span class="best-price">\s*(R\$ [\d,\.]+)\s*</span>', product_html)

            old_price = old_price_match.group(1) if old_price_match else None
            best_price = best_price_match.group(1) if best_price_match else None

            # Determinando o preço a ser usado
            price = best_price if best_price else old_price if old_price else 'Preço não disponível'

            yield {
                'brand': brand,
                'name': name,
                'price': price,
                'old_price': old_price,  # Incluindo o preço antigo se disponível
            }

        # Paginando se houver mais produtos na categoria
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)