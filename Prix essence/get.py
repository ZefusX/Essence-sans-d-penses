import requests
import json

def get_specs(departement):
    response = requests.get(f'https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records?limit=-1&refine=departement%3A"{departement}"')
    data_dict = json.loads(response.text)
    return data_dict

def split_dico(dico):
    for x,y in dico.items():
        total_count = x
        dico_results = y
    return dico_results

def afficher_donnees(data):
    results = []
    for liste_dico in data:
        if isinstance(liste_dico, dict):
            for key, value in liste_dico.items():
                results.append(f"{key}: {value}")
    return results

def afficher_important(data):
    liste_important = ["latitude","longitude","adresse","ville","gazole_prix", "sp95_prix", "e85_prix", "gplc_prix", "e10_prix", "sp98_prix"]
    ls=[]
    for element in data:
        for i in range(len(liste_important)):
            if liste_important[i] in element:
                ls.append(element)
    result = []
    current_sublist = []
    for element in ls:
        if "latitude" in element:
            if current_sublist:  # Ajoute la sous-liste courante à la liste résultat si elle n'est pas vide
                result.append(current_sublist)
            current_sublist = [element]  # Commence une nouvelle sous-liste avec l'élément actuel
        else:
            current_sublist.append(element)
    if current_sublist:
        result.append(current_sublist)  # Ajoute la dernière sous-liste à la liste résultat si elle n'est pas vide
    return result

def extraire_prix(string):
    liste_carbu = ["gazole", "sp95", "e85", "gplc", "e10", "sp98"]
    for i in range(len(liste_carbu)):
        if liste_carbu[i] in string:
            debut_prix = string.rfind(' ') + 1
    return string[debut_prix:]
    
def trouver_prix_moins_cher(data, carburant):
    prix_min_carburant = float(999999.0)
    min_carburant_sublist = None
    for element in data:
        for i in range(len(element)):
            if carburant in element[i] and not "None" in element[i]:
                current_price = float(extraire_prix(element[i]))
                if current_price < prix_min_carburant:
                    prix_min_carburant = current_price
                    min_carburant_sublist = element

    return min_carburant_sublist

def supp_doublons(ls):
    ls_clean = []
    for sous_liste in ls:
        sous_liste_clean = []
        for element in sous_liste:
            if element not in sous_liste_clean:
                sous_liste_clean.append(element)
        ls_clean.append(sous_liste_clean)
    return ls_clean


def extraire_loc(sous_liste):
    lat = sous_liste[0]
    long = sous_liste[1]

    lat = ''.join(c for c in lat if c.isdigit() or c == '.')
    long = ''.join(c for c in long if c.isdigit() or c == '.')
    lat = lat.split('.')[0]
    long = long.split('.')[0]
    lat = lat[:2] + "." + lat[2:]
    long = long[:1] + "." + long[1:]
    return lat, long

def info_a_afficher(sous_liste):
    ls_infos = []
    ls_infos = sous_liste[2:]
    return ls_infos


if __name__=="__main__":

    print(extraire_loc(['latitude: 4925636.7262787', 'longitude: 613017.46660705', 'adresse: RUE CLEMENCEAU', 'ville: Amnéville', 'gazole_prix: 1.739', 'sp95_prix: 1.759', 'e85_prix: 0.985', 'gplc_prix: None', 'e10_prix: 1.729', 'sp98_prix: None']))
    # dico_prix = get_specs("Moselle")
    # dico_prix = split_dico(dico_prix)

    # result_list = afficher_donnees(dico_prix)

    # ls_important = afficher_important(result_list)
    # ls_important_clean = supp_doublons(ls_important)
    # print(ls_important_clean)

    # liste_carbu = ["gazole", "sp95", "e85", "gplc", "e10", "sp98"]
    # carburant_choisi = 'gazole'

    # prix_moins_cher = trouver_prix_moins_cher(ls_important_clean, carburant_choisi)
    # print(prix_moins_cher)
