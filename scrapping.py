import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://www.imdb.com/search/title/"
params = {
    "genres": "Action",
    "explore": "genres",
    "title_type": "feature",
    "ref_": "ft_movie_0"
}


films = []


max_pages = 5

# Boucle pour itérer sur les pages de résultats
page_number = 1
while page_number <= max_pages:
    # Ajouter le numéro de page aux paramètres de l'URL
    params["start"] = (page_number - 1) * 50

   
    response = requests.get(base_url, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu de la page
        soup = BeautifulSoup(response.content, "html.parser")

        # Trouver tous les conteneurs de films sur la page
        movie_containers = soup.find_all("div", class_="lister-item-content")

        # Vérifier s'il y a des films sur la page
        if len(movie_containers) == 0:
            break  

        # Parcourir chaque conteneur de film et extraire les informations
        for container in movie_containers:
            
            title = container.find("h3", class_="lister-item-header").a.text

           
            genre = container.find("span", class_="genre").text.strip()

            
            year = container.find("span", class_="lister-item-year").text.strip("()")

           
            duration_element = container.find("span", class_="runtime")
            duration = duration_element.string.strip() if duration_element else ""

            
            actors = container.find("p", class_="").find_all("a")
            actor_names = [actor.text for actor in actors]

            # Ajouter les informations du film à la liste
            film_info = {
                "Titre": title,
                "Genre": genre,
                "Année de sortie": year,
                "Durée": duration,
                "Acteurs": ", ".join(actor_names)
            }
            films.append(film_info)

        # Passer à la page suivante
        page_number += 1

    else:
        print("La requête a échoué avec le code d'état :", response.status_code)
        break

# Écrire les informations des films dans un fichier CSV
csv_file = "films.csv"

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["Titre", "Genre", "Année de sortie", "Durée", "Acteurs"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Écrire l'en-tête du fichier CSV

    for film in films:
        writer.writerow(film)

print("Les informations des films ont été écrites dans"), csv
