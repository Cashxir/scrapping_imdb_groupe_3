import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder

def get_movie_data():
    return pd.read_csv("films.csv")

def main():
    movies = get_movie_data()
    X = movies.drop("Titre", axis=1)  # Variables prédictives (Genre, Année de sortie, Durée, Acteurs)
    y = movies["Titre"]  # Variable cible (Titre du film)

    # Encodage des variables catégorielles
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)

    clf = DecisionTreeClassifier()
    clf.fit(X_encoded, y)

    genre = input("Quel genre de film avez-vous envie de regarder ? ")
    decade = input("Préférez-vous les films d'une époque en particulier ? ")
    duration = input("Combien de temps auriez-vous à accorder au film ? ")
    actor = input("Quel acteur affectionnez-vous ? ")

    # Encodage des caractéristiques du film à recommander
    movie_features = pd.DataFrame({"Genre": [genre], "Année de sortie": [decade], "Durée": [duration], "Acteurs": [actor]})
    movie_features_encoded = encoder.transform(movie_features)

    recommended_movie = clf.predict(movie_features_encoded)
    print("Je vous recommande de regarder :", recommended_movie[0])

main()
