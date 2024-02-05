import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def crawl_website(url):

    #Faz a requisição HTTP para obter o conteúdo do site

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.get_text(separator='\n', strip=True))
    text = soup.get_text(separator='\n', strip=True)
    #print(text)
    client = OpenAI(api_key='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')

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "Seja analisador de textos e conceda os sentimentos dos textos"},
            {"role": "user", "content": text}])
    print(completion.choices[0].message)


crawl_website('https://petcare.com.br/')



    