import requests
from bs4 import BeautifulSoup
import pdfkit
from openai import OpenAI

class WebsiteCrawler:
    def __init__(self, url, api_key, output_file, max_chars=2000):
        self.url = url
        self.api_key = api_key
        self.output_file = output_file
        self.max_chars = max_chars

    def crawl(self, ai_command):
        try:
            response = requests.get(  self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            maintag = soup.find('main')
            if maintag is None:
                maintag = soup
            text = maintag.get_text(separator='\n', strip=True)

            if len(text) > self.max_chars:
                text = text[:self.max_chars]

            client = OpenAI(api_key=self.api_key)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": ai_command},
                    {"role": "user", "content": text}
                ])
            result.content = completion.choices[0].message

            print(result.content)
            pdfkit.from_string(result.content, self.output_file, configuration=config)

        except Exception as e:
            return f"Erro ao processar a URL: {str(e)}"

# Configuração do PDF
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Testando com diferentes URLs e comandos
meucrawler = "Seja um analisador de textos e responda somente as categorias do que se trata o texto no formato de tags com hashtags"
minhaurl = 'https://docs.python.org/pt-br/3/tutorial/index.html'
crawler1 = WebsiteCrawler(minhaurl, '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', 'output_meucrawler.pdf')
resultado = crawler1.crawl(meucrawler)

meuprofessor = 'Seja meu professor de python'
crawler2 = WebsiteCrawler(minhaurl, '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', 'output_meuprofessor.pdf')
result = crawler2.crawl(meuprofessor)

print(resultado, result)