.. MTGDC-BANLIST documentation master file, created by
   sphinx-quickstart on Sat Aug  5 23:54:20 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenue dans la document du module MTGDC-BANLIST!
===================================================

De manière plus ou moins régulière à travers l'histoire du format,
les annonces de **Banned and Restricted** permettent de savoir quelles
cartes sont légales ou non dans le format.

Stockées dans le dossier ``<racine>/banlists/``, les annonces sont stockées au
format JSON

.. code-block:: JSON

    [
        {
            "date": "2015-07-17",
            "summary": "Over the last three months, Duel Commander events have been more numerous and more populated. The player activity on all media was also very intensive. Such dynamics are very positive for the format and we hope that it will keep on going.",
            "newly_banned_as_commander": [],
            "newly_unbanned_as_commander": [],
            "newly_banned_in_deck": ["Mystical Tutor"],
            "newly_unbanned_in_deck": [],
            "explanations": {
                "Mystical Tutor": "Mystical Tutor is a card that really favoured combo and control decks to the detriment of aggressive decks, which is the opposite of the re-balancing decisions that our comitee turns to. Some of its interactions were formidable (miracle keyword cards) and it was really making players take too much advantage over the 99 unique cards rule, allowing players to include powerful but situational cards (like Armageddon / Upheaval) with lesser risks. Seeing it banned also opens other unbans in the long run."
            }
        }
    ]

.. note::

   Il est possible de contribuer au maintien des fichiers de banlist en se rendant sur `GitHub <https://github.com/barrins-codex/mtgdc-banlist>`_.

Module ``mtgdc_banlist``
========================

.. automodule:: mtgdc_banlist.__main__
   :members:

Classe ``BanlistCompiler``
==========================

.. autoclass:: mtgdc_banlist.banlist_compiler.BanlistCompiler
   :members:
