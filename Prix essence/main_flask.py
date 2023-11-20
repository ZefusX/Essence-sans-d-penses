from flask import Flask, render_template, request
from get import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    localisation = None 
    infos = None

    if request.method == 'POST':
        department = request.form['department']
        carburant = request.form['carburant']

        result = trouver_prix_moins_cher(supp_doublons(afficher_important(afficher_donnees(split_dico(get_specs(department))))), carburant)
        localisation = extraire_loc(result)
        infos = info_a_afficher(result)

    return render_template('home.html', result=result, localisation=localisation, infos=infos)

if __name__ == '__main__':
    app.run(debug=True)