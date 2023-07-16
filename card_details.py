import re

import requests
from unidecode import unidecode


def clear_text(string: str):
    string = re.sub(r"\&amp;", "", string)
    string = re.sub(r" - Art$", "", string)  # When importing deck from MTGTOP8
    string = re.sub(r"^A-", "", string)  # When importing deck from MTGTOP8
    string = unidecode(string).lower()
    string = re.sub(r"[^a-zA-Z0-9]", "", string)
    return string


def scryfall_data(nom_carte):
    carte = clear_text(nom_carte)
    criteres = "%28legal%3Aduel+or+restricted%3Aduel+or+banned%3Aduel%29"
    criteres = criteres + "+is%3Afirstprint"
    url = f"https://api.scryfall.com/cards/search?q={criteres}+{carte}"
    reponse = requests.get(url, stream=True)
    resultat = reponse.json()
    data = resultat["data"]
    if "has_more" in resultat.keys():
        for line in data:
            if clear_text(line["name"]) == carte:
                return line
            # Example case : Sheoldred // The True Scriptures
            if (line["name"][: len(nom_carte)] == nom_carte) and (
                line["name"][len(nom_carte) : len(nom_carte) + 4] == " // "
            ):
                return line
            # Example case : Needleverge Pathway // Pillarverge Pathway
            if (line["name"][-len(nom_carte) :] == nom_carte) and (
                line["name"][-(len(nom_carte) + 4) : -len(nom_carte)] == " // "
            ):
                return line
    return data


def card_data(nom_carte):
    carte = scryfall_data(nom_carte)

    return {
        "id": carte["oracle_id"],
        "nom": nom_carte,
        "release": carte["released_at"],
        "scryfall": carte["id"],
    }
