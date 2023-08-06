"""
project.parser

Fichier permettant d'utiliser le parser et d'executer la compilation demandée.
"""
import argparse

parser = argparse.ArgumentParser(
    prog="create_banlist.py",
    description=(
        "Le fichier permet de compiler les banlists "
        + "présentes dans le dossier `./banlists`"
    ),
    epilog=(
        "Il est possible de contribuer au projet sur GitHub: "
        + "https://github.com/barrins-codex/mtgdc-banlist"
    ),
)

parser.add_argument(
    "--compile-json",
    action="store_true",
    help="Génère la version actuelle de la banlist au format JSON",
)
parser.add_argument(
    "--compile-html",
    action="store_true",
    help="Génère l'historique de la banlist au format HTML",
)
parser.add_argument(
    "--compile-both", action="store_true", help="Génère les fichiers JSON et HTML"
)
