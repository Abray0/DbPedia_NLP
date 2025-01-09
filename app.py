from flask import Flask, request, jsonify,render_template
from services.dbpedia_service import DBPediaService

# Initialize Flask app and DBPediaService
app = Flask(__name__)
dbpedia_service = DBPediaService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_movies():
    """Endpoint to search for movies."""
    data = request.json
    search_term = data.get('query', '').strip()

    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400

    try:
        results = dbpedia_service.search_movies(search_term)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/relations', methods=['POST'])
def movie_relations():
    """Endpoint to fetch relations for a movie."""
    data = request.json
    movie_uri = data.get('movie_uri', '').strip()

    if not movie_uri:
        return jsonify({'error': 'Movie URI is required'}), 400

    try:
        relations = dbpedia_service.fetch_movie_relations(movie_uri)
        return jsonify({'relations': relations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
