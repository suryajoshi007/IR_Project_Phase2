from flask import Flask, request, jsonify
from query import QueryProcessor

app = Flask(__name__)

@app.before_request
def initialize_query_processor():
    app.query_processor = QueryProcessor(
        input_corpus="./data/input_corpus.txt"
    )

@app.route('/testing', methods=['GET'])
def testing():
    return "Hello world from Flask app", 200

@app.route('/execute_query', methods=['POST'])
def process_queries():
    try:
        data = request.get_json()
        if 'queries' in data and isinstance(data['queries'], list):
            queries = data['queries']
            ans = app.query_processor.get_final_struct(queries=queries)
            return jsonify(ans), 200
        else:
            return jsonify(
                {'error': 'Invalid JSON format or missing "queries" key'}
            ), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9999, debug=True)
