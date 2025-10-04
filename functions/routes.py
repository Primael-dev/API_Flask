#Importation des librairies importantes
from flask import Flask, request

#importation des fonctions depuis le fichier methods.py contenu dans functions
from functions.models import *

def app():
    #création de l'instance de l'applicaation Flask
    app=Flask(__name__)


    #route de la racine et la fonction de bienvenue sur l'api
    @app.route('/api')
    def hello():
        return 'Hello world!! My API is Running...'


    #route concernant les methods 'post' et 'get' pour affichage de tout les livres et ajout d'un livre
    @app.route('/api/v1/livres', methods=['GET','POST'])
    def views_books():

        #vérifications des methods afin d'exécuter le bon code
        
        if request.method=='GET':
            return get_books()
        
        if request.method=='POST':
            return post_book()
        
    #route concernant les méthods 'get' (ce get pour un livre unique), 'put', 'delete' et 'patch' . L'url utilise l'id du livre 
    @app.route('/api/v1/livres/<book_id>',methods=['GET','PUT','DELETE','PATCH'])
    def single_book(book_id):

        #vérifications des methods afin d'exécuter le bon code

        if request.method=='GET':
            return book_view(book_id)
        
        if request.method=='PUT':
            return update_book(book_id)

        if request.method=='DELETE':
            return book_delete(book_id)
        
        if request.method=='PATCH':
            return patching_book(book_id)

    return app