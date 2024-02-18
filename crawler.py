import requests
from bs4 import BeautifulSoup
import pdfkit
from openai import OpenAI

def crawl_website(url, ai_comando, max_chars=2000):
    try:
        # Faz a requisição HTTP para obter o conteúdo do site
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        maintag = soup.find('main')
        if maintag is None:
            maintag = soup
        text = maintag.get_text(separator='\n', strip=True)

        # Ajusta o limite de caracteres com base no tamanho real do texto
        if len(text) > max_chars:
            text = text[:max_chars]

        # Conexão com a API OpenAI e obtenção da resposta
        client = OpenAI(api_key='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')
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[
                {"role": "system", "content": ai_comando},
                {"role": "user", "content": text}
            ])
        result = completion.choices[0].message
        
        # Gerar arquivo PDF
        pdfkit.from_string(result, 'output.pdf')
        return result
    except Exception as e:
        return f"Erro ao processar a URL: {str(e)}"

# Testando com diferentes URLs e comandos
meucrawler = "Seja um analisador de textos e responda somente as categorias do que se trata o texto no formato de tags com hashtags"
minhaurl = 'https://docs.python.org/pt-br/3/tutorial/index.html' 
resultado = crawl_website(minhaurl, meucrawler)

meuprofessor = 'Seja meu professor de python'
result = crawl_website(minhaurl, meuprofessor)

print(resultado, result)

