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

    def busca_dados(self):
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

            return text

        except Exception as e:
            return f"Erro ao buscar dados: {str(e)}"

    def processa_dados(self, ai_command, text):
        try:
            client = OpenAI(api_key=self.api_key)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": ai_command},
                    {"role": "user", "content": text}
                ])

            result_content = completion.choices[0].message
            return f"Erro ao processar os dados: {str(e)}"

    def analisa_dados(self, result_content):
        

    def salva_dados(self, result_content):
        try:
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdfkit.from_string(result.content, self.output_file, configuration=config)

            return "Dados salvos com sucesso!!!"

        except Exception as e:

            return f"Erro ao salvar os dados:" {str(e)}

    def crawl(self, ai_command):
        text = self.busca_dados()

# Testando com diferentes URLs e comandos
meucrawler = "Seja um analisador de textos e responda somente as categorias do que se trata o texto no formato de tags com hashtags"
minhaurl = 'https://docs.python.org/pt-br/3/tutorial/index.html'
crawler1 = WebsiteCrawler(minhaurl, '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', 'output_meucrawler.pdf')
resultado = crawler1.crawl(meucrawler)

meuprofessor = 'Seja meu professor de python'
crawler2 = WebsiteCrawler(minhaurl, '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', 'output_meuprofessor.pdf')
result = crawler2.crawl(meuprofessor)

print(resultado, result)