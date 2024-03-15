from crawler import WebsiteCrawler

minhaurl = 'https://docs.python.org/pt-br/3/tutorial/index.html'

crawler = WebsiteCrawler()

meucrawler = "Seja um analisador de textos e responda somente as categorias do que se trata o texto no formato de tags com hashtags"
crawler.crawl(meucrawler, minhaurl, 'output_meucrawler.pdf')

'''meuprofessor = 'Seja meu professor de python e faça um resumo do texto'
crawler.crawl(meuprofessor, minhaurl, 'output_meuprofessor.pdf')'''

'''result = crawler.analisa_dados('Seja meu professor', 'Quem é você?')

print(result)'''