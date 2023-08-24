"""
L'objectif principale de ce module est de compiler les banlists
présentes dans le dossier ``<racine>/banlists/`` et d'en générer
la version actuelle au format JSON : ::

   python mtgdc_banlist --compile-json

Il est aussi possible de créer une vue HTML récapitulant l'historique
des bans du format avec les mouvements de la banlist et les
justifications : ::

   python mtgdc_banlist --compile-html

Les deux fonctionnalitées peuvent être réalisées en simultané lors de
l'appel au module : ::

   python mtgdc_banlist --compile-both

.. note::

    L'utilisation des deux options ``--compile-json`` et
    ``compile-html`` produit le même résultat que ``compile-both`` : ::

        python mtgdc_banlist --compile-json --compile-html
"""
import sys

from mtgdc_banlist.banlist_compiler import BanlistCompiler
from mtgdc_banlist.parser import parser


def main(args):
    """
    Procédure pricipale qui gère le retour du parser.

    La procédure appelle la classe ``BanlistCompiler`` pour récupérer
    les informations demandées : soit le fichier JSON, soit le fichier
    HTML, soit les deux.

    Les fichiers sont ensuite créés/modifiés selon le chemin fourni.

    :param args list: Liste des arguments à parser
    """
    args = parser.parse_args(args)

    if not any([args.compile_json, args.compile_html, args.compile_both]):
        parser.print_help()

    banlist = BanlistCompiler()

    if any([args.compile_json, args.compile_both]):
        banlist.get_json_banlist(args.output)

    if any([args.compile_html, args.compile_both]):
        banlist.compile_to_html(args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
