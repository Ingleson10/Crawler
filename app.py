from flask import Flask, render_template, request, jsonify
from crawler import WebsiteCrawler
import os

app = Flask(__name__)
crawler = WebsiteCrawler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rastreamento', methods=['POST'])
def rastreamento():
    url = request.form['url']
    ai_command = request.form['ai_command']
    output_file = request.form['output_file']
    
    crawler.rastrear(ai_command, [url], [output_file])
    
    return jsonify({"status": "Rastreamento completo, verifique os arquivos de saída."})

# Rotas adicionais baseadas no arquivo `server.py`

@app.route('/rastreamento/iniciar', methods=['POST'])
def iniciar_rastreamento():
    data = request.get_json()
    ai_command = data.get('ai_command')
    url = data.get('url')
    output_file = data.get('output_file')

    if not all([ai_command, url, output_file]):
        return jsonify({'error': 'Parâmetros necessários ausentes'}), 400

    crawler.rastrear(ai_command, [url], [output_file])
    return jsonify({'message': 'Rastreamento iniciado com sucesso!'})

@app.route('/rastreamento/pesquisar', methods=['GET'])
def pesquisar_rastreamento():
    return jsonify({'message': 'Pesquisando dados rastreados!'})

@app.route('/rastreamento/atualizar', methods=['PUT'])
def atualizar_rastreamento():
    data = request.get_json()
    ai_command = data.get('ai_command')
    url = data.get('url')
    output_file = data.get('output_file')

    if not all([ai_command, url, output_file]):
        return jsonify({'error': 'Parâmetros necessários ausentes'}), 400

    crawler.rastrear(ai_command, [url], [output_file])
    return jsonify({'message': 'Parâmetros de rastreamento atualizados com sucesso!'})

@app.route('/rastreamento/cancelar', methods=['DELETE'])
def cancelar_rastreamento():
    return jsonify({'message': 'Processo de rastreamento cancelado!'})

@app.route('/rastreamento/status', methods=['GET'])
def status_rastreamento():
    status = "Funcionalidade de status não implementada"
    return jsonify({'status': status})

if __name__ == '__main__':
    os.makedirs('pdf', exist_ok=True)
    os.makedirs('csv', exist_ok=True)
    os.makedirs('json', exist_ok=True)
    app.run(debug=True)