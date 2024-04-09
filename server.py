import os
from flask import Flask, jsonify, request
from crawler import WebsiteCrawler  # Importando a classe WebsiteCrawler

app = Flask(__name__)
crawler = WebsiteCrawler()

# Rota POST para iniciar o crawling
@app.route('/crawl/initiating', methods=['POST'])
def crawl():
    data = request.get_json()
    ai_command = data.get('ai_command')
    url = data.get('url')
    output_file = data.get('output_file')

    if not all([ai_command, url, output_file]):
        return jsonify({'error': 'Missing required parameters'}), 400

    crawler.crawl(ai_command, url, output_file)  # Chamando a função crawl do crawler

    # Após o crawling, gerar o PDF
    pdf_file_path = f'pdf/{output_file}'
    if os.path.exists(pdf_file_path):
        return jsonify({'message': 'Crawling initiated successfully and PDF generated!'})
    else:
        return jsonify({'error': 'PDF generation failed!'}), 500

# Rota GET para pesquisar dados crawleados
@app.route('/crawl/search', methods=['GET'])
def search_crawl():
    # Implemente a lógica de pesquisa, se necessário
    pass

# Rota PUT para atualizar parâmetros do crawling
@app.route('/crawl/update', methods=['PUT'])
def update_crawl():
    data = request.get_json()
    ai_command = data.get('ai_command')
    url = data.get('url')
    output_file = data.get('output_file')

    if not all([ai_command, url, output_file]):
        return jsonify({'error': 'Missing required parameters'}), 400

    crawler.update_crawl(ai_command, url, output_file)  # Chamando a função update_crawl do crawler
    return jsonify({'message': 'Crawling parameters updated successfully!'})

# Rota DELETE para cancelar o processo de crawling
@app.route('/crawl/cancel', methods=['DELETE'])
def cancel_crawl():
    crawler.cancel_crawl()  # Chamando a função cancel_crawl do crawler
    return jsonify({'message': 'Crawling process cancelled!'})

# Rota GET para verificar o status do crawling
@app.route('/crawl/status', methods=['GET'])
def crawl_status():
    status = crawler.get_crawl_status()  # Chamando a função get_crawl_status do crawler
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=True)