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
import json
import sys

from mtgdc_banlist.banlist_compiler import BanlistCompiler
from mtgdc_banlist.parser import parser


def main(args):
    """Fonction pricipale qui gère le retour du parser.

    La fonction appelle la classe ``BanlistCompiler`` pour récupérer
    les informations demandées : soit le fichier JSON, soit le fichier
    HTML, soit les deux.

    :param args list: Liste des arguments à parser

    :returns: fichier(s) selon le(s) paramètre(s) en argument
    :rtype: Tuple(dict, list)
    """
    args = parser.parse_args(args)

    """
    if not any([args.compile_json, args.compile_html, args.compile_both]):
        parser.print_help()
    """

    banlist = BanlistCompiler()
    with open("test.txt", "+w") as file:
        json.dump(banlist._json, file, indent=4, sort_keys=True, ensure_ascii=False)

    json_file = None
    html_file = None

    if any([args.compile_json, args.compile_both]):
        json_file = banlist.get_json_banlist(args.output)

    if any([args.compile_html, args.compile_both]):
        banlist.compile_to_html(args.output)

    return

if __name__ == "__main__":
    print(main(sys.argv[1:]))
