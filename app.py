from functions.routes import app

#condition de lancement
if __name__=='__main__':

    #création de l'objet flask
    app_run=app()
    #lancement du serveur flask
    app_run.run(debug=True)