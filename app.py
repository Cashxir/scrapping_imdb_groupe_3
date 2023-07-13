import http.server
import socketserver
import json
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        movie_data = json.loads(post_data)

        genre = movie_data['genre']
        decade = movie_data['decade']
        duration = movie_data['duration']
        actor = movie_data['actor']

        movies = get_movie_data()
        X = movies.drop("Titre", axis=1)
        y = movies["Titre"]

        encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        X_encoded = encoder.fit_transform(X)

        clf = DecisionTreeClassifier()
        clf.fit(X_encoded, y)

        movie_features = pd.DataFrame({"Genre": [genre], "Année de sortie": [decade], "Durée": [duration], "Acteurs": [actor]})
        movie_features_encoded = encoder.transform(movie_features)

        recommended_movie = clf.predict(movie_features_encoded)
        response = recommended_movie[0]

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

def get_movie_data():
    return pd.read_csv("films.csv")

def main():
    PORT = 8000
    Handler = RequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()

if __name__ == '__main__':
    main()
