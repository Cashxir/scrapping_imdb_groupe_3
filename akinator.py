import pandas as pd
import re

# Classe représentant un nœud de l'arbre de décision
class NoeudDecision:
    def __init__(self, question, oui_noeud=None, non_noeud=None):
        self.question = question
        self.oui_noeud = oui_noeud
        self.non_noeud = non_noeud

# Fonction pour poser une question à l'utilisateur et obtenir une réponse "oui" ou "non"
def poser_question(question):
    reponse = input(question + " (oui/non) : ").lower()
    while reponse != "oui" and reponse != "non":
        print("Veuillez répondre par 'oui' ou 'non'.")
        reponse = input(question + " (oui/non) : ").lower()
    return reponse == "oui"

# Fonction pour charger les films depuis un fichier CSV
def charger_films(nom_fichier):
    df = pd.read_csv(nom_fichier)
    films = df.to_dict("records")
    return films

# Fonction pour rechercher un film en utilisant l'arbre de décision
def rechercher_film(noeud, film):
    if isinstance(noeud, str):
        # Le nœud est une feuille contenant le nom du film
        print("Le film que vous cherchez est :", noeud)
    else:
        reponse = poser_question(noeud.question)
        if reponse:
            if noeud.oui_noeud is not None:
                rechercher_film(noeud.oui_noeud, film)
            else:
                print("Aucun film correspondant trouvé.")
        else:
            if noeud.non_noeud is not None:
                rechercher_film(noeud.non_noeud, film)
            else:
                print("Aucun film correspondant trouvé.")

# Vérifie si la durée d'un film est supérieure à 120 minutes
def verifier_duree(film):
    duree = film["Durée"]
    if isinstance(duree, str) and duree.endswith("min"):
        duree = int(duree[:-3])  # Extrait le nombre de la durée
        return duree > 120
    return False

# Vérifie si l'année de sortie d'un film est récente (à partir de 2021)
def verifier_recent(film):
    annee_sortie = film["Année de sortie"]
    annee_sortie = re.sub(r'\D', '', str(annee_sortie))  # Supprime les caractères non numériques
    try:
        annee = int(annee_sortie[:4])
        return annee >= 2021
    except ValueError:
        return False

# Chargement des films depuis le fichier CSV
films = charger_films("films.csv")

# Création de l'arbre de décision pour la recherche de films
racine = NoeudDecision("Le film est-il un film d'action ?")
noeud_duree = NoeudDecision("Le film dure-t-il plus de 120 minutes ?", None, None)
noeud_recent = NoeudDecision("Le film est-il récent ?", noeud_duree, None)
racine.oui_noeud = noeud_recent

# Construction de l'arbre de décision en fonction des valeurs réelles de la base de données
for film in films:
    if "Action" in film["Genre"]:
        if verifier_recent(film):
            if verifier_duree(film):
                if noeud_duree.oui_noeud is None:
                    noeud_duree.oui_noeud = film["Titre"]
            else:
                if noeud_duree.non_noeud is None:
                    noeud_duree.non_noeud = film["Titre"]

# Lancement de la recherche de films en utilisant l'arbre de décision
rechercher_film(racine, films)
