from flask import Flask, render_template, request
from get import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    localisation = None 
    infos = None

    if request.method == 'POST':
        recherche = request.form['department']
        carburant = request.form['carburant']

        if is_departement(recherche)==True:
            result = trouver_prix_moins_cher(supp_doublons(afficher_important(afficher_donnees(split_dico(get_specs_departement(recherche))))), carburant)
        else:
            result = trouver_prix_moins_cher(supp_doublons(afficher_important(afficher_donnees(split_dico(get_specs_city(recherche))))), carburant)
            
        localisation = extraire_loc(result)
        infos = info_vraiment_importante(result,carburant)

    return render_template('home.html', result=result, localisation=localisation, infos=infos)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")