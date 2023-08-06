"""
project.banlist_compiler
"""
import glob
import json


class BanlistCompiler:
    """
    Cette classe permet de travailler les fichiers JSON disponibles dans
    le répertoire ``<racine>/banlists/``.

    .. code-block :: python

        >>> from mtgdc_banlist.banlist_compiler import BanlistCompiler
        >>> banlist = BanlistCompiler()
        >>>
        >>> # Know if a card is banned via a call to `is_banned` function
        >>> print(banlist.is_banned("Snow-covered Island"))
        >>> False
        >>>
        >>> print(banlist.is_banned("Fblthp, the Lost", command_zone=True))
        >>> False
        >>>
        >>> # Know if a card is banned via a call to `md_bans` property for
        >>> # bans in the main deck:
        >>> print("Snow-covered Island" in banlist.md_bans)
        >>> False
        >>>
        >>> # Know if a card is banned via a call to `cz_bans` property for
        >>> # bans in the command zone:
        >>> print("Fblthp, the Lost" in banlist.cz_bans)
        >>> False
    """

    def __init__(self):
        self._json = {}
        self._dates = []
        self._current = None

        for file in glob.glob("banlists" + "/*.json"):
            with open(file, "r", encoding="utf-8") as json_file:
                date_annonce = file.split("/", maxsplit=1)[1][:-5]
                self._dates.append(date_annonce)
                self._json[date_annonce] = json.load(json_file)[0]

        self._dates = sorted(self._dates)

        self._walk()

    def _walk(self):
        """
        Fonction qui vérifie date par date les mouvements de la banlist.

        :meta private:
        """
        cz_bans = set()
        md_bans = set()
        for date in self._dates:
            cz_bans = cz_bans | set(self._json[date]["newly_banned_as_commander"])
            cz_bans = cz_bans - set(self._json[date]["newly_unbanned_as_commander"])
            md_bans = md_bans | set(self._json[date]["newly_banned_in_deck"])
            md_bans = md_bans - set(self._json[date]["newly_unbanned_in_deck"])

        self._current = {
            "banned_commanders": list(cz_bans),
            "banned_cards": list(md_bans),
        }
        return self._current

    def get_json_banlist(self):
        """
        Fonction qui retourne la banliste au format JSON.

        :returns: La liste des cartes bannies dans les entrées
            ``banned_commandes`` et ``banned_cards``
        :rtype: Dict"""
        return self._current

    def _add_tooltip(self, text, tooltip):
        """
        Fonction qui permet de rajouter le tooltip au nom de la carte

        :param text str: Phrase à laquelle ajouter un tooltip
        :param tooltip str: Contenu du tooltip

        :returns: Text avec tooltip prêt à intégrer dans le fichier HTML
        :rtype: str

        :meta private:
        """
        return (
            f'<a href="#" data-bs-toggle="tooltip" data-bs-title="{tooltip}">{text}</a>'
        )

    def _changes(self, json_data, zone):
        """
        Fonction qui retourne les mouvements concernés dans la banliste (``json_data``)
        selon la ``zone`` indiquée.

        :param json_data dict: Données chargées depuis un fichier dans
            ``<racine>/banlists/<fichier>.json``
        :param zone str: (``md`` ou ``cz``) correspond à la zone souhaitée

        :returns: La liste des mouvements (bans et unbans) pour la zone
        :rtype: dict

        :meta private:
        """
        choice = "as_commander" if zone == "cz" else "in_deck" if zone == "md" else ""
        precision = " as a commander" if choice == "as_commander" else ""

        bans = [
            (
                "<li>"
                + self._add_tooltip(card, json_data["explanations"][card])
                + f" is now <strong>banned</strong>{precision}."
                + "</li>"
            )
            for card in json_data[f"newly_banned_{choice}"]
        ]
        unbans = [
            (
                "<li>"
                + self._add_tooltip(card, json_data["explanations"][card])
                + f" is now <strong>unbanned</strong>{precision}."
                + "</li>"
            )
            for card in json_data[f"newly_unbanned_{choice}"]
        ]

        return bans + unbans

    def _create_html_card(self, json_data):
        """
        Fonction qui permet de créer la carte ``timeline`` concernant la
        banlist fournie.

        :param json_data dict: Données chargées depuis un fichier dans
            ``<racine>/banlists/<fichier>.json``

        :returns: La carte prête à intégrer dans le code HTML de la page
        :rtype: str

        :meta private:
        """

        card = '<div class="timeline">'
        card += '<span class="timeline-icon"></span>'
        card += f'<span class="year">{json_data["date"]}</span>'
        card += '<div class="timeline-content">'
        card += f'<p class="description">{json_data["summary"]}</p>'

        end_card = "</div></div>"

        cz_changes=self._changes(json_data, zone="cz")
        md_changes=self._changes(json_data, zone="md")

        if all([len(cz_changes) == 0, len(md_changes) ==0]):
            card += '<h3 class="title">No Changes</h3>'
            return card + end_card

        if len(cz_changes) > 0:
            card += '<h3 class="title">Changes in Command Zone</h3>'
            for change in cz_changes:
                card += change

        if len(md_changes) > 0:
            card += '<h3 class="title">Changes in Deck</h3>'
            for change in md_changes:
                card += change

        return card + end_card

    def compile_to_html(self):
        """Fonction qui retourne l'historique au format HTML."""
        return [
            self._create_html_card(self._json[date])
            for date in self._dates
        ]

    def is_banned(self, card, command_zone=False):
        """
        Fonction qui évalue la présence de ``card`` dans la banlist.

        Par défaut, la fonction ne recherche que dans les bans du
        main deck mais il est possible d'utiliser ``command_zone=True``
        lors de l'appel pour chercher dans les généraux bannis.

        :param card str: Carte dont la présence sur la banlist est évaluée
        :param command_zone bool: Indique si la recherche se situe dans
            les cartes bannies en tant que commandat(e).

        :returns: La présence de la carte dans la liste évaluée
        :rtype: bool
        """
        if command_zone:
            return card in self.cz_bans
        else:
            return card in self.md_bans

    @property
    def md_bans(self):
        """
        Propriété qui fournit la liste des cartes bannies dans le deck.

        :returns: La liste des cartes bannies dans le main deck
        :rtype: List
        """
        return self._current["banned_cards"]

    @property
    def cz_bans(self):
        """
        Propriété qui fournit la liste des cartes bannies en tant que
        commandant(e).

        :returns: La liste des cartes bannies dans la zone de commandement
        :rtype: List
        """
        return self._current["banned_commanders"]
