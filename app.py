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

if __name__ == '__main__':
    os.makedirs('pdf', exist_ok=True)
    os.makedirs('csv', exist_ok=True)
    os.makedirs('json', exist_ok=True)
    app.run(debug=True)