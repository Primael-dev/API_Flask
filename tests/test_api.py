#importation nécessaires
import json

#Tests pour l'API de gestion des livres
class TestAPIBooks:
    
    #Test de la route de bienvenue
    def test_hello_route(self, client):

        #simulation de get
        response = client.get('/api')

        #verification du code et de la presence du message
        assert response.status_code == 200
        assert b'Hello world!! My API is Running...' in response.data
    
    #Test de l'affichage de tt les livres
    def test_get_all_books(self, client):

        #simulation de get de tt les livres
        response = client.get('/api/v1/livres')

        #verification du code
        assert response.status_code == 200

        #transfromartion en objet python
        data = json.loads(response.data)

        #verification du'il s'agit d'une liste
        assert isinstance(data, list)
        assert len(data) >= 0

    #Test d'ajout d'un livre
    def test_post_book(self, client):

        #requete
        new_book = {
            "title": "Nouveau Livre",
            "author": "Nouvel Auteur",
            "year": 2024
        }

        #envoie d'une requete post avc les données
        response = client.post(
            '/api/v1/livres',
            data=json.dumps(new_book),
            content_type='application/json'
        )

        #verification du code
        assert response.status_code == 201

        #transformation en objet
        data = json.loads(response.data)
        assert 'id' in data
        assert data['title'] == "Nouveau Livre"
        assert data['author'] == "Nouvel Auteur"


    #test de données post invalide
    def test_post_book_invalid_data(self, client):

        #envoie d'une requete post avec données invalide
        response = client.post(
            '/api/v1/livres',
            data='invalid json',
            content_type='application/json'
        )
        #vérification de la reponse
        assert response.status_code in [400,500]

    #Test de récupération d'un livre spécifique
    def test_get_single_book(self, client):

        #envoie de la requete et vérification du code
        response = client.get('/api/v1/livres/0')
        assert response.status_code == 200

        #tranformation en objet python
        data = json.loads(response.data)
        assert data['id'] == 0

    #Test de récupération d'un livre inexistant
    def test_get_nonexistent_book(self, client):

        #requete
        response = client.get('/api/v1/livres/9999')

        #verification du code et transformation en objet
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    #Test de récupération d'un livre inexistant
    def test_get_book_invalid_id(self, client):

        #requete invalide
        response = client.get('/api/v1/livres/abc')
        
        #verification du code
        assert response.status_code == 400

    #Test de remplacement complet d'un livre
    def test_update_book_put(self, client):
        
        #json valide
        updated_book = {
            "title": "Livre Modifié",
            "author": "Auteur Modifié",
            "year": 2023
        }

        #requete
        response = client.put(
            '/api/v1/livres/0',
            data=json.dumps(updated_book),
            content_type='application/json'
        )

        #verification du code et transformation en objet
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == "Livre Modifié"
        assert data['id'] == 0  

    #Test de remplacement complet d'un livre
    def test_patch_book(self, client):
        
        #mis à jour
        patch_data = {"title": "Titre Modifié Partiellement"}

        #requete
        response = client.patch(
            '/api/v1/livres/0',
            data=json.dumps(patch_data),
            content_type='application/json'
        )

        #verification du code et tranformation en objet
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == "Titre Modifié Partiellement"
        assert 'author' in data  

    #Test que l'ID ne peut pas être modifié via PATCH
    def test_patch_book_cannot_change_id(self, client):
        
        #json et requete
        patch_data = {"id": 9999, "title": "Test"}
        response = client.patch(
            '/api/v1/livres/0',
            data=json.dumps(patch_data),
            content_type='application/json'
        )
        
        #verification du coder et trancformation en objet
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 0  

    #Test de suppression d'un livre
    def test_delete_book(self, client):
        
        #requete et verification du code
        response = client.delete('/api/v1/livres/1')
        assert response.status_code == 204
        
        # Vérification que le livre n'existe plus
        response = client.get('/api/v1/livres/1')
        assert response.status_code == 404

    #Test de suppression d'un livre inexistant
    def test_delete_nonexistent_book(self, client):
        
        #reuete et verification du code
        response = client.delete('/api/v1/livres/9999')
        assert response.status_code == 404