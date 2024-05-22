import requests
from bs4 import BeautifulSoup
import pdfkit
import csv
import json
from textblob import TextBlob
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

chave_openai = os.getenv('CHAVE_OPENAI')

class WebsiteCrawler:
    def __init__(self, chave_api=chave_openai, max_chars=2000):
        self.chave_api = chave_api
        self.max_chars = max_chars

    def rastrear(self, comando_ai, urls, arquivos_saida):
        if not self.chave_api:
            print("Chave da API não encontrada. Por favor, defina a chave da API do OpenAI.")
            return
        
        if len(urls) != len(arquivos_saida):
            print("Erro: Número de URLs e arquivos de saída devem ser iguais.")
            return
        
        for url, arquivo_saida in zip(urls, arquivos_saida):
            print(f'Processando {url}...')
            texto_encontrado = self.buscar_dados(url)
            if texto_encontrado:
                texto_processado = self.processar_dados(texto_encontrado)
                if texto_processado:
                    texto_analisado = self.analisar_dados(comando_ai, texto_processado)
                    if texto_analisado:
                        self.salvar_dados(arquivo_saida, texto_analisado, texto_processado)
        print('Concluído!!!')

    def buscar_dados(self, url):
        print(f'Buscando {url}...')
        try:
            resposta = requests.get(url)
            resposta.encoding = resposta.apparent_encoding
            resposta.raise_for_status()
            return resposta.text
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados de {url}: {str(e)}")
            return None

    def processar_dados(self, texto):
        print('Processando...')
        try:
            soup = BeautifulSoup(texto, 'html.parser')
            tag_principal = soup.find('main')

            if tag_principal is None:
                tag_principal = soup
            texto = tag_principal.get_text(separator='\n', strip=True)

            if len(texto) > self.max_chars:
                texto = texto[:self.max_chars]

            return texto

        except Exception as e:
            print(f"Erro ao processar dados: {str(e)}")
            return None

    def analisar_dados(self, comando_ai, texto):
        print('Analisando...')
        
        cliente = OpenAI(api_key=self.chave_api)
        try:
            conclusao = cliente.chat.completions.create(
                    model="gpt-3.5-turbo", messages=[
                        {"role": "system", "content": comando_ai},
                        {"role": "user", "content": texto}
                    ])
            resultado_conteudo = conclusao.choices[0].message
            return resultado_conteudo.content
        except Exception as e:
            print(f"Erro ao analisar dados: {str(e)}")
            return None

    def analisar_sentimento(self, texto):
        print('Analisando sentimento...')
        try:
            blob = TextBlob(texto)
            sentimento = blob.sentiment
            return {'polarity': sentimento.polarity, 'subjectivity': sentimento.subjectivity}
        except Exception as e:
            print(f"Erro ao analisar sentimento: {str(e)}")
            return None

    def salvar_dados(self, arquivo_saida, resultado_conteudo, texto_processado):
        print(f'Salvando {arquivo_saida}...')
        try:
            # Analisar sentimento
            sentimento = self.analisar_sentimento(texto_processado)

            # Configurar pdfkit com wkhtmltopdf
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            options = {
                'encoding': 'UTF-8',
                'enable-local-file-access': True
            }
            pdfkit.from_string(resultado_conteudo, f'pdf/{arquivo_saida}.pdf', configuration=config, options=options)

            # Salvar sentimento como CSV e JSON
            with open(f'csv/{arquivo_saida}.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Texto', 'Polaridade', 'Subjetividade'])
                writer.writerow([texto_processado, sentimento['polarity'], sentimento['subjectivity']])

            with open(f'json/{arquivo_saida}.json', mode='w', encoding='utf-8') as file:
                json.dump({'texto': texto_processado, 'polaridade': sentimento['polarity'], 'subjetividade': sentimento['subjectivity']}, file, ensure_ascii=False, indent=4)

            print(f"Dados salvos com sucesso em pdf/{arquivo_saida}.pdf, csv/{arquivo_saida}.csv, json/{arquivo_saida}.json!!!")
        except Exception as e:
            print(f"Erro ao salvar dados em {arquivo_saida}: {str(e)}")