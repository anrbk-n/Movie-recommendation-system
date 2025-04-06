from flask import Flask, render_template, request
import pandas as pd
from fuzzywuzzy import process  
from transformers import pipeline  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack

app = Flask(__name__)

df = pd.read_csv('C:/Users/Niyaz/Downloads/clean_tmdb_movies.csv')

def extract_genres(genre_names):
    return genre_names.split(',') if genre_names else ['Unknown']

corrector = pipeline("text2text-generation", model="t5-small")

def correct_text(text):
    corrected_text = corrector(text, max_length=50)[0]['generated_text']
    return corrected_text

def transliterate_to_english(input_text):
    translit_map = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']',
        'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';', 'э': "'",
        'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
        'А': 'Q', 'Б': 'W', 'В': 'E', 'Г': 'R', 'Д': 'T', 'Е': 'Y', 'Ё': 'U', 'Ж': 'I', 'З': 'O', 'И': 'P', 'Й': '{', 'К': '}',
        'Л': 'A', 'М': 'S', 'Н': 'D', 'О': 'F', 'П': 'G', 'Р': 'H', 'С': 'J', 'Т': 'K', 'У': 'L', 'Ф': ':', 'Х': '"',
        'Ц': 'Z', 'Ч': 'X', 'Ш': 'C', 'Щ': 'V', 'Ь': 'B', 'Ы': 'N', 'Э': 'M', 'Ю': '<', 'Я': '>'
    }
    translated_text = ''.join([translit_map.get(char, char) for char in input_text])
    return translated_text

def fuzzy_search_movie(user_input, df, limit=10, threshold=70):
    user_input_transliterated = transliterate_to_english(user_input)
    corrected_input = correct_text(user_input_transliterated)
    user_input_lower = corrected_input.lower()
    movie_titles = df['title'].tolist()
    matches = process.extract(user_input_lower, movie_titles, limit=limit)
    filtered_matches = [match for match in matches if match[1] >= threshold]
    matched_movies = df[df['title'].isin([match[0] for match in filtered_matches])]
    return matched_movies, filtered_matches
#MAIN
@app.route('/', methods=['GET', 'POST'])
def index():
    movies_data = []
    for _, row in df.head(10).iterrows():  
        movie = {
            'id': row['id'],
            'title': row['title'],
            'poster_path': row['poster_path'],
            'overview': row['overview'],
            'release_date': row['release_date'],
            'genres': extract_genres(row['genre_names']),
            'vote_average': row['vote_average']
        }
        movies_data.append(movie)
    return render_template('index.html', movies=movies_data)

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    matches, suggestions = fuzzy_search_movie(search_query, df)
    movies_data = []
    for _, row in matches.iterrows():
        movie = {
            'id': row['id'],
            'title': row['title'],
            'poster_path': row['poster_path'],
            'overview': row['overview'],
            'release_date': row['release_date'],
            'genres': extract_genres(row['genre_names']),
            'vote_average': row['vote_average']
        }
        movies_data.append(movie)
    return render_template('results.html', movies=movies_data, suggestions=suggestions)

@app.route('/load_more', methods=['GET'])
def load_more():
    start = int(request.args.get('start', 10))
    end = start + 10
    movies_data = []
    for _, row in df[start:end].iterrows():
        movie = {
            'id': row['id'],
            'title': row['title'],
            'poster_path': row['poster_path'],
            'overview': row['overview'],
            'release_date': row['release_date'],
            'genres': extract_genres(row['genre_names']),
            'vote_average': row['vote_average']
        }
        movies_data.append(movie)
    return render_template('movie_part.html', movies=movies_data)

def create_combined_features(row):
    return (
            str(row['genre_names'] or '') + ' ' +
            str(row['overview'] or '') + ' ' +
            str(row['cast'] or '') + ' ' +
            str(row['crew'] or '') + ' ' +
            str(row['production_companies'] or '') + ' ' +
            str(row['production_countries'] or '') + ' ' +
            str(row['spoken_languages'] or '') + ' ' +
            str(row['original_language'] or '')
    )


# vectorize
def vectorize_features(df):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    feature_matrix = vectorizer.fit_transform(df['combined_features'])

    genre_vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    genre_matrix = genre_vectorizer.fit_transform(df['genre_names'])

    feature_matrix = hstack([feature_matrix, genre_matrix])

    return feature_matrix
df['combined_features'] = df.apply(create_combined_features, axis=1)

feature_matrix = vectorize_features(df)

#cosine_sim
cosine_sim = cosine_similarity(feature_matrix, feature_matrix)


def get_recommendations(title, cosine_sim=cosine_sim):
    title = title.lower()  # Convert to lowercase

    if title not in df['title'].str.lower().values:
        return f"Movie '{title}' not found in the database."

    idx = df[df['title'].str.lower() == title].index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Skip the movie itself

    movie_indices = [i[0] for i in sim_scores]

    return df.iloc[movie_indices][['title', 'id']].to_dict(orient='records')

@app.route('/movie_details/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movie = df[df['id'] == movie_id].iloc[0]
    movie_data = {
        'id': movie['id'],
        'title': movie['title'],
        'release_date': movie['release_date'],
        'vote_average': movie['vote_average'],
        'overview': movie['overview'],
        'poster_path': movie['poster_path'],
        'original_language': movie['original_language'],
        'genres': movie['genre_names'].split(', '),
        'popularity': movie['popularity'],
        'vote_count': movie['vote_count'],
        'backdrop_path': movie['backdrop_path'],
        'original_title': movie['original_title'],
        'adult': movie['adult'],
        'video': movie['video'],
        'production_companies': movie['production_companies'],
        'production_countries': movie['production_countries'],
        'runtime': movie['runtime'],
        'spoken_languages': movie['spoken_languages'],
        'budget': movie['budget'],
        'revenue': movie['revenue'],
        'status': movie['status'],
        'tagline': movie['tagline'],
        'imdb_id': movie['imdb_id'],
        'cast': movie['cast'],
        'crew': movie['crew'],
        'combined_text': movie['combined_text']
    }

    recommendations = get_recommendations(movie['title'])

    if isinstance(recommendations, str):
        print(recommendations)  
        return render_template('movie_details.html', movie=movie_data, recommended_movies=[])
    else:
        return render_template('movie_details.html', movie=movie_data, recommended_movies=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

