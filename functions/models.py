#importer les bibliotheques nécessaires
from flask import request,jsonify

#importation des fonctions depuis le fichier manage.py contenu dans functions
from functions.manage import load_books, save_book


#fonction d'affichage de tt les livres
def get_books():

    #chargement des livres et retournement sous format json
    books=load_books()
    return jsonify(books)

#fonction d'ajout d'un livre
def post_book():
    try:
        #recuperation de la requete sous format json
        data=request.get_json()

        #verification que les donnés sont présentes et qu'il sont des dictionnaire, retour de code erreur 400
        if not data or not isinstance(data,dict):
            return jsonify({"error":"json data missing"}),400
        
        #chargement des livres
        books=load_books()

        #Id du nouveau livre grace à len
        new_id=len(books)

        #création du nouveau livre
        new_book={**data,'id':new_id}

        #ajout du nouveau livre
        books.append(new_book)

        #sauveagarde des livres
        save_book(books)

        #retournement du livre créé ainsi que le code 201 created
        return jsonify(new_book),201
    
    #gestion et capture des erreurs
    except Exception as e:
        return jsonify({'error':f'{e}'}),500
    

#fonction d'affichage d'un seul livre en lui passant l'id
def book_view(book_id):
    
    try:
        #chargement du livre et conversion de l'id en entier
        books=load_books()
        book_id=int(book_id)

        #utilisation de next qui recherche et retourne le premier livre correspondant sinon None
        search_book=next((book for book in books if book.get('id')==book_id),None)

        #vérification que le livre existe
        if search_book:
            # si oui retourner le livre sous format Json
            return jsonify(search_book)
        else:
            # si non retourner erreur et code erreur 404
            return jsonify({'error':f'Book with ID {book_id} not found'}),404
        
    #capture l'erreur si l'id n'est pas un nombre
    except ValueError:
        return jsonify({'error':'Invalid format'}),400
    
    #capture les exceptions
    except Exception as e:
        return jsonify({'error':f'{e}'}),500
    

#fonction de suppression de livre via id
def book_delete(book_id):
    try:
        book_id= int(book_id)
    
    #capture des erreurs et en cas d'erreur rupture de la suite
    except ValueError:
        return jsonify({'error':'invalid format'}),400
    
    try:
        #chargement des livres
        books=load_books()

        #rechercher le livre a supprimé
        delete_book=next((i for i,book in enumerate(books) if book.get('id')==book_id),None)

        #verification que l'index a été trouvé
        if delete_book is None:
            return jsonify({'error':f'Book with ID{book_id} not found'}),404
        
        #suppression du livre
        books.pop(delete_book)
        save_book(books)

        #retourner Ok et le code 204
        return 'OK',204
    
    #capture les exceptions
    except Exception as e:
        return jsonify({'error':f'{e}'}),500
    


#fonction de remplacement du livre entier sauf id 
def update_book(book_id):
    try:
        book_id=int(book_id)

        #capture de format invalide
    except ValueError:
        return jsonify({'error':'invalid format'}),400
    
    #recuperation de la requete sous format json
    new_book=request.get_json()

    #verification que les donnés sont présentes et qu'il sont des dictionnaire, retour de code erreur 400
    if not new_book or not isinstance(new_book,dict):
        return jsonify({'error':'invalid format json'}),400
    
    #chargement des livres
    books=load_books()

    #rechercher le livre a mettre à jour
    book_update=next((i for i,book in enumerate(books) if book.get('id')==book_id),None)

    #verification que l'index a été trouvé
    if book_update is None:
        return jsonify({'error':f'The book with ID {book_id} was not found'}),404
    
    books[book_update]=new_book

    #conservation de l'id
    books[book_update]['id'] = book_id

    #variable de référencre
    updated_book=books[book_update]

    #sauvegarde des livres
    save_book(books)

    #retounement su livre mis à jour et code 200, Ok
    return jsonify(updated_book),200

#fonction de mis à jour
def patching_book(book_id):

    try:
        book_id=int(book_id)

        #capture de format invalide
    except ValueError:
        return jsonify({'error':'invalid format'}),400
    
    #recuperation de la requete sous format json
    book_modif=request.get_json()

    #verification que les donnés sont présentes et qu'il sont des dictionnaire, retour de code erreur 400
    if not book_modif or not isinstance(book_modif,dict):
        return jsonify({'error':'invalid format json'}),400
    
    #bloquer la modification de l'id pour les utilisateur zarb
    if 'id' in book_modif:
        del book_modif['id']

    #chargement des livres
    books=load_books()

    #rechercher le livre a mettre à jour
    book_index=next((i for i,book in enumerate(books) if book.get('id')==book_id),None)

    #verification que l'index a été trouvé
    if book_index is None:
        return jsonify({'error':f'The book with ID {book_id} was not found'}),404

    #reference au livre
    exist_book= books[book_index]

    #fusion des champs modififier
    exist_book.update(book_modif)

    #sauvegarde des livres
    save_book(books)

    #retournement du livre et code 200
    return jsonify(exist_book),200