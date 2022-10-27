# Outil de création d'un fichier comprenant les polygones du Centre Val de Loire et
# des départements limitrophes, pour utilisation par le frontend (carte détourée
# dans l'écran new_trip). Cette construction ne doit avoir lieu qu'une seule fois
# (sauf si les périmètres des départements changent !) et c'est la raison pour laquelle
# le code est stocké ici, avec celui de la constitution du fichier d'adresses (qui, lui,
# peut être relancé régulièrement en se fondant sur des fichiers d'adresses départementaux
# régulièrement actualisés).
#
#
#
# Olivier - Juin 2022 (lorsqu'est apparue la nécessité d'étendre le périmètre de saisie
# des adresses aux départements voisins)
#
import os, json

# On récupère le chemin du répertoire dans lequel se trouve le présent fichier
basedir = os.path.abspath(os.path.dirname(__file__))


def build_polygon_files() :
    """ Construit un fichier polygon pour chacun des fichiers geojson territoriaux"""

    # terr_list = ['essonne', 'yvelines', 'eure', 'orne', 'sarthe', 'maine-et-loire', 'vienne', 'haute-vienne', 'creuse', 'allier', 'nievre', 'yonne', 'seine-et-marne']
    terr_list = ['maine-et-loire', 'vienne', 'haute-vienne', 'creuse', 'allier', 'nievre', 'yonne', 'seine-et-marne']
    # terr_list = ['essonne', 'yvelines', 'eure', 'orne', 'sarthe']
    # terr_list = ['404227461']
    # Pour chacun des territoires de la liste...
    for terr in terr_list :
        print(terr)
        # ...on extrait la valeur de la clé geometry depuis le json contenu dans le fichier territorial...
        with open(basedir + "/" + terr + ".geojson", 'r') as terr_file :
            terr_dict = json.load(terr_file)
            terr_lng_lat_coordinates = terr_dict["geometry"]["coordinates"][0]
            terr_lat_lng_coordinates = [[coord[1], coord[0]] for coord in terr_lng_lat_coordinates]
            lat_lng_terr_dict = {"lat_lng_coordinates" : terr_lat_lng_coordinates}
        with open(basedir + "/" + terr + "-latlng.json", 'w') as lat_lng_terr_file :
            json.dump(lat_lng_terr_dict, lat_lng_terr_file)


if __name__ == "__main__":
    build_polygon_files()
