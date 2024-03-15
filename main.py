from crawler import WebsiteCrawler

meucrawler = "Seja um analisador de textos e responda somente as categorias do que se trata o texto no formato de tags com hashtags"
minhaurl = 'https://docs.python.org/pt-br/3/tutorial/index.html'
crawler1 = WebsiteCrawler(minhaurl, 'output_meucrawler.pdf')
resultado = crawler1.crawl(meucrawler)

meuprofessor = 'Seja meu professor de python'
crawler2 = WebsiteCrawler(minhaurl, 'output_meuprofessor.pdf')
result = crawler2.crawl(meuprofessor)

print(resultado, result)