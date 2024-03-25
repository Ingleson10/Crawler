from crawler import WebsiteCrawler

def main():
    # URL que será rastreada
    minha_url = 'https://docs.python.org/pt-br/3/tutorial/index.html'
    
    # Inicializa o rastreador do site
    crawler = WebsiteCrawler()

    # Configuração do primeiro rastreador
    meucrawler_config = {
        'description': "Seja um analisador de textos e responda somente as categorias do que se trata o texto no formato de tags com hashtags",
        'output_file': 'output_meucrawler.pdf'
    }
    # Executa o rastreamento
    crawler.crawl(minha_url, **meucrawler_config)

'''meuprofessor = 'Seja meu professor de python e faça um resumo do texto'
crawler.crawl(meuprofessor, minhaurl, 'output_meuprofessor.pdf')'''

'''result = crawler.analisa_dados('Seja meu professor', 'Quem é você?')

print(result)'''