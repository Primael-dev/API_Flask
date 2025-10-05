#importer les librairies nécessaires
import json
from pathlib import Path
import os


#indication du chemin du fichier json 'livres.json'
json_filename = os.environ.get('BOOKS_JSON_FILE', 'livres.json')
Json_file=Path(__file__).parent.parent/json_filename


#fonction de lecture du fichier 'livres.json'
def load_books():
    
    try:
        #lecture du contenu du fichier 'livres;json'
        data_json=Json_file.read_text(encoding='utf-8')

        data=json.loads(data_json)

        #le if verifie qu'il s'agit d'une liste
        return data if isinstance(data,list)else []
    
    #capture des erreurs fichier introuvable et erreurs de decodage
    except (FileNotFoundError,json.JSONDecodeError,IOError):

        return []
    

#fonction de sauvegarde du fichier 'Livres.json'
def save_book(books_list):
    Json_file.write_text(json.dumps(books_list,indent=4),encoding='utf-8')