import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def crawl_website(url, ai_comando):

    #Faz a requisição HTTP para obter o conteúdo do site

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser') # vai buscar códigos em HTML e fazer leitura.
    maintag = soup.find('main')
    #print(maintag)
    if maintag is None: #None palavra reservada
        maintag = soup
    #print(soup.get_text(separator='\n', strip=True))
    text = maintag.get_text(separator='\n', strip=True)
    text = text[:2000]
    #print(text)
    #return text # verificar quantidade de caracteres para consumo de API.
    client = OpenAI(api_key='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')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": ai_comando},
            {"role": "user", "content": text}])

    return completion.choices[0].message

#result = crawl_website('https://petcare.com.br/')

#print(result)

meucrawler = "Seja um analisador de textos e responda somente as categorias do que se trata o texto no formato de tags com hashtags"

minhaurl = 'https://docs.python.org/pt-br/3/tutorial/index.html' 

resultado = crawl_website(minhaurl, meucrawler)

meuprofessor = 'Seja meu professor de python'

result = crawl_website(minhaurl, meuprofessor)

print(resultado, result)
    