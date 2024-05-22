import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pdfkit
import csv
import json
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

load_dotenv()

# Acessar variáveis de ambiente
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

chave_openai = os.getenv('CHAVE_OPENAI')

class WebsiteCrawler:
    def __init__(self, chave_api=chave_openai, max_chars=2000, max_workers=5):
        self.chave_api = chave_api
        self.max_chars = max_chars
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
    def __del__(self):
        if self.conn:
            self.conn.close() # Fechar a conexão com o banco de dados ao destruir o objeto
            
    def conectar_bd(self):
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            return conn
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def criar_tabela_historico(self):
        try:
            conn = self.conectar_bd()
            if conn:
                cursor = conn.cursor()
                create_table_query = """
                CREATE TABLE IF NOT EXISTS historico (
                    id SERIAL PRIMARY KEY,
                    url TEXT,
                    comando_ai TEXT,
                    arquivo_saida TEXT,
                    pdf_file BYTEA,
                    csv_file TEXT,
                    json_file TEXT,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                conn.commit()
                cursor.close()
                conn.close()
                print('Tabela "historico" criada com sucesso!')
        except Exception as e:
            print(f"Erro ao criar a tabela 'historico': {str(e)}")
            
    def salvar_historico(self, url, comando_ai, arquivo_saida):
        try:
            cursor = self.conn.cursor()
            
            # Inserir os dados no banco de dados
            cursor.execute("INSERT INTO historico (url, comando_ai, arquivo_saida) VALUES (%s, %s, %s)", (url, comando_ai, arquivo_saida))

            # Confirmar a transação
            self.conn.commit()

            print('Histórico salvo com sucesso!')
        except psycopg2.Error as e:
            print(f"Erro ao salvar histórico: {e}")

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
    
    def analisar_sentimento(self, texto):
        print('Analisando Sentimento...')
        try:
            blob = TextBlob(texto)
            sentimento = blob.sentiment
            return {'polarity': sentimento.polarity, 'subjectivity': sentimento.subjectivity}
        except Exception as e:
            print(f"Erro ao analisar sentimento: {str(e)}")

    def processar_url(self, comando_ai, url, arquivo_saida):
        print(f'Processando {url}...')
        texto_encontrado, dados_estruturados = self.buscar_dados(url)
        if texto_encontrado:
            texto_processado = self.processar_dados(texto_encontrado)
            if texto_processado:
                texto_analisado = self.analisar_dados(comando_ai, texto_processado)
                if texto_analisado:
                    sentimento = self.analisar_sentimento(texto_processado)
                    if sentimento:
                        self.salvar_dados(arquivo_saida, texto_analisado, dados_estruturados, sentimento)

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

    def salvar_dados(self, arquivo_saida, resultado_conteudo, dados_estruturados, sentimento):
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
            
            # Salvar sentimento como CSV
            with open(f'csv/{arquivo_saida}_sentimento.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Texto', 'Polaridade', 'Subjetividade'])
                writer.writerow([resultado_conteudo, sentimento['polarity'], sentimento['subjectivity']])
            print(f"Sentimento salvo com sucesso em csv/{arquivo_saida}_sentimento.csv!!!")
        
            # Salvar sentimento como JSON
            with open(f'json/{arquivo_saida}_sentimento.json', mode='w', encoding='utf-8') as file:
                json.dump({'texto': resultado_conteudo, 'polaridade': sentimento['polarity'], 'subjetividade': sentimento['subjectivity']}, file, ensure_ascii=False, indent=4)
            print(f"Sentimento salvo com sucesso em json/{arquivo_saida}_sentimento.json!!!")
        
        except Exception as e:
            print(f"Erro ao salvar dados em {arquivo_saida}: {str(e)}")