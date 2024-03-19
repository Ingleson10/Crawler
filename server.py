from flask import Flask, jsonify, request
from crawler import WebsiteCrawler

app = Flask(__name__)
crawler = WebsiteCrawler()

# POST route for initiating crawling
@app.route('/crawl/initiating', methods=['POST'])
def crawl():
    data = request.get_json()
    ai_command = data.get('ai_command')
    url = data.get('url')
    output_file = data.get('output_file')

    if not all([ai_command, url, output_file]):
        return jsonify({'error': 'Missing required parameters'}), 400

    crawler.crawl(ai_command, url, output_file)
    return jsonify({'message': 'Crawling initiated successfully!'})

# GET route for searching crawled data
@app.route('/crawl/search', methods=['GET'])
def search_crawl():
    request.args.get('ai_command')
    request.args.get('url')
    request.args.get('output_file')

# PUT route for updating crawling parameters
@app.route('/crawl/update', methods=['PUT'])
def update_crawl():
    data = request.get_json()
    ai_command = data.get('ai_command')
    url = data.get('url')
    output_file = data.get('output_file')

    if not all([ai_command, url, output_file]):
        return jsonify({'error': 'Missing required parameters'}), 400

    crawler.update_crawl(ai_command, url, output_file)
    return jsonify({'message': 'Crawling parameters updated successfully!'})

# DELETE route for canceling crawling process
@app.route('/crawl/cancel', methods=['DELETE'])
def cancel_crawl():
    crawler.cancel_crawl()
    return jsonify({'message': 'Crawling process cancelled!'})

# GET route for checking crawling status
@app.route('/crawl/status', methods=['GET'])
def crawl_status():
    status = crawler.get_crawl_status()
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=True)