import requests
from bs4 import BeautifulSoup
import pdfkit
import csv
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

load_dotenv()

chave_openai = os.getenv('CHAVE_OPENAI')

class WebsiteCrawler:
    def __init__(self, chave_api=chave_openai, max_chars=2000, max_workers=5):
        self.chave_api = chave_api
        self.max_chars = max_chars
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def rastrear(self, comando_ai, urls, arquivos_saida):
        if not self.chave_api:
            print("Chave da API não encontrada. Por favor, defina a chave da API do OpenAI.")
            return
        
        if len(urls) != len(arquivos_saida):
            print("Erro: Número de URLs e arquivos de saída devem ser iguais.")
            return
        
        tasks = []
        for url, arquivo_saida in zip(urls, arquivos_saida):
            tasks.append(self.executor.submit(self.processar_url, comando_ai, url, arquivo_saida))
        
        for task in tasks:
            task.result()
        
        print('Concluído!!!')

    def processar_url(self, comando_ai, url, arquivo_saida):
        print(f'Processando {url}...')
        texto_encontrado, dados_estruturados = self.buscar_dados(url)
        if texto_encontrado:
            texto_processado = self.processar_dados(texto_encontrado)
            if texto_processado:
                texto_analisado = self.analisar_dados(comando_ai, texto_processado)
                if texto_analisado:
                    self.salvar_dados(arquivo_saida, texto_analisado, dados_estruturados)

    @lru_cache(maxsize=128)
    def buscar_dados(self, url):
        print(f'Buscando {url}...')
        try:
            resposta = requests.get(url)
            resposta.encoding = resposta.apparent_encoding
            resposta.raise_for_status()
            soup = BeautifulSoup(resposta.text, 'html.parser')
            texto = resposta.text
            dados_estruturados = self.extrair_dados_estruturados(soup)
            return texto, dados_estruturados
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados de {url}: {str(e)}")
            return None, None

    def extrair_dados_estruturados(self, soup):
        dados_estruturados = {
            'tables': [],
            'products': []
        }
        
        # Extraindo tabelas
        for tabela in soup.find_all('table'):
            headers = [header.get_text(strip=True) for header in tabela.find_all('th')]
            rows = []
            for row in tabela.find_all('tr'):
                cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            if headers and rows:
                dados_estruturados['tables'].append({'headers': headers, 'rows': rows})

        # Extraindo listas de produtos (exemplo para ul > li)
        for lista in soup.find_all('ul'):
            produtos = [item.get_text(strip=True) for item in lista.find_all('li')]
            if produtos:
                dados_estruturados['products'].append(produtos)
        
        return dados_estruturados

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

    def salvar_dados(self, arquivo_saida, resultado_conteudo, dados_estruturados):
        print(f'Salvando {arquivo_saida}...')
        try:
            # Salvar PDF
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            options = {
                'encoding': 'UTF-8',
                'enable-local-file-access': True
            }
            pdfkit.from_string(resultado_conteudo, f'pdf/{arquivo_saida}.pdf', configuration=config, options=options)
            print(f"Dados salvos com sucesso em pdf/{arquivo_saida}.pdf!!!")
            
            # Salvar dados estruturados como CSV
            csv_arquivo = f'csv/{arquivo_saida}.csv'
            os.makedirs(os.path.dirname(csv_arquivo), exist_ok=True)
            with open(csv_arquivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for tabela in dados_estruturados['tables']:
                    writer.writerow(tabela['headers'])
                    writer.writerows(tabela['rows'])
                    writer.writerow([])  # Linha em branco entre tabelas
            print(f"Dados estruturados salvos com sucesso em {csv_arquivo}!!!")
            
            # Salvar dados estruturados como JSON
            json_arquivo = f'json/{arquivo_saida}.json'
            os.makedirs(os.path.dirname(json_arquivo), exist_ok=True)
            with open(json_arquivo, mode='w', encoding='utf-8') as file:
                json.dump(dados_estruturados, file, ensure_ascii=False, indent=4)
            print(f"Dados estruturados salvos com sucesso em {json_arquivo}!!!")
            
        except Exception as e:
            print(f"Erro ao salvar dados em {arquivo_saida}: {str(e)}")