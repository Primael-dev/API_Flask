#importation nécessaires
import pytest
import sys
from pathlib import Path
import os
from functions.routes import app as create_app
from functions.manage import save_book


# Ajout du répertoire racine du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# mise en place de la varaible d'environnement car au premier test sans cela mes 50 livres ont disapru
os.environ['BOOKS_JSON_FILE'] = 'livres_test.json'

#defifinition de la fixture app
@pytest.fixture
def app():
    
    #création de l'instance de l'apk flask
    flask_app = create_app()

    #il s'agit d'un test
    flask_app.config['TESTING'] = True
    return flask_app

#definition de la fixture client
@pytest.fixture
def client(app):

    #création de client de test
    return app.test_client()

#definition de la fixture runner
@pytest.fixture
def runner(app):

    #création d'un lanceur de commandes CLI
    return app.test_cli_runner()

#definitionn de la fisture setup_test_data
@pytest.fixture(autouse=True)
def setup_test_data():
    #Initialisation les données de test avant chaque test
    # Créer des données de test
    test_books = [
        {"id": 0, "title": "Test Book 1", "author": "Author 1", "year": 2020},
        {"id": 1, "title": "Test Book 2", "author": "Author 2", "year": 2021}
    ]
    save_book(test_books)
    
    yield