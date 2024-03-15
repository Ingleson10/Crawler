import requests
from bs4 import BeautifulSoup
import pdfkit
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

chatgpt_key = os.getenv('CHATGPT_KEY')

class WebsiteCrawler:
    def __init__(self, api_key=chatgpt_key, max_chars=2000):
        self.api_key = api_key
        self.max_chars = max_chars

    def crawl(self, ai_command, url, output_file):
        print('Inicializando...')
        text_buscado = self.busca_dados(url)
        text_processado = self.processa_dados(text_buscado)
        if text_processado:
            text_analisado = self.analisa_dados(ai_command, text_processado)
            self.salva_dados(output_file,text_analisado)
        
        print('Finalizado!!!')

    def busca_dados(self, url):
        print('Buscando...')
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            response.raise_for_status()
            return response.text
        except Exception as e:
            return f"Erro ao buscar dados: {str(e)}"  

    def processa_dados(self, text):
        print('Processando...')
        try:
            soup = BeautifulSoup(text, 'html.parser')
            maintag = soup.find('main')

            if maintag is None:
                maintag = soup
            text = maintag.get_text(separator='\n', strip=True)

            if len(text) > self.max_chars:
                text = text[:self.max_chars]

            return text

        except Exception as e:
            return f"Erro ao processar os dados: {str(e)}"

    def analisa_dados(self, ai_command, text):
        print('Analisando...')
        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": ai_command},
                    {"role": "user", "content": text}
                ])

        result_content = completion.choices[0].message
        return result_content.content

    def salva_dados(self, output_file, result_content):
        print('Salvando...')
        try:
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            options = {
                'encoding': 'UTF-8',
                'enable-local-file-access': True
            }
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdfkit.from_string(result_content, f'pdf/{output_file}', configuration=config, options=options)

            return "Dados salvos com sucesso!!!"

        except Exception as e:
            return f"Erro ao salvar os dados: {str(e)}"


