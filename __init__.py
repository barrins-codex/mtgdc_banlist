import glob
import html
import json
import os
from datetime import datetime

import pkg_resources


class BanlistCompiler:
    def __init__(self):
        self._json = {}
        self._dates = []
        self._current = None

        banlists_path = pkg_resources.resource_filename("mtgdc_banlist", "banlists")
        json_files = glob.glob(os.path.join(banlists_path, "*.json"))
        for file in json_files:
            with open(file, "r", encoding="utf-8") as json_file:
                date_annonce = file.split("/", maxsplit=1)[1][:-5]
                self._dates.append(date_annonce)
                self._json[date_annonce] = json.load(json_file)[0]

        self._dates = sorted(self._dates, reverse=True)

        self._walk()

    def _walk(self):
        cz_bans = set()
        md_bans = set()
        for date in sorted(self._dates):
            cz_bans = cz_bans | set(self._json[date]["newly_banned_as_commander"])
            cz_bans = cz_bans - set(self._json[date]["newly_unbanned_as_commander"])
            md_bans = md_bans | set(self._json[date]["newly_banned_in_deck"])
            md_bans = md_bans - set(self._json[date]["newly_unbanned_in_deck"])

        self._current = {
            "banned_commanders": sorted(list(cz_bans)),
            "banned_cards": sorted(list(md_bans)),
        }

        return self._current

    def get_json_banlist(self, output_file):
        output_file = "banlists.json" if output_file == "" else output_file

        with open(output_file, "+w", encoding="utf-8") as banlist_file:
            json.dump(
                self._current,
                banlist_file,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )

    def _add_tooltip(self, text, tooltip_dict):
        tooltip = ""

        if text in tooltip_dict.keys():
            tooltip = tooltip_dict[text]
            tooltip = html.escape(tooltip)

        return f'<span class="card-banlist" data-tooltip="{tooltip}">{text}</span>'

    def _changes(self, json_data, zone):
        choice = "as_commander" if zone == "cz" else "in_deck" if zone == "md" else ""
        precision = " as a commander" if choice == "as_commander" else ""

        bans = [
            (
                self._add_tooltip(card, json_data["explanations"])
                + f" is now <strong>banned</strong>{precision}."
                + "<br>"
            )
            for card in sorted(json_data[f"newly_banned_{choice}"])
        ]
        unbans = [
            (
                self._add_tooltip(card, json_data["explanations"])
                + " is now <strong>legal</strong>."
                + "<br>"
            )
            for card in sorted(json_data[f"newly_unbanned_{choice}"])
        ]

        return bans + unbans

    def _date_to_str(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        month_name = date_obj.strftime("%B")
        year = date_obj.strftime("%Y")
        day = date_obj.strftime("%d")
        day_suffix = (
            "th"
            if 11 <= int(day) <= 13
            else {1: "st", 2: "nd", 3: "rd"}.get(int(day) % 10, "th")
        )

        return f"{month_name} {year}, {day}{day_suffix}"

    def _create_html_card(self, json_data):

        card = '<div class="timeline">'

        link = ""
        if "link" in json_data.keys():
            link = f'<a href="{json_data["link"]}" title="Go to the official '
            link += 'announcement"><i class="fa-solid fa-link"></i></a>'
        card += f'<span class="timeline-icon">{link}</span>'

        if json_data["date"] == "Previous bans":
            card += f'<span class="year">{json_data["date"]}</span>'
        else:
            card += f'<span class="year">{self._date_to_str(json_data["date"])}</span>'

        card += '<div class="timeline-content">'

        changes = '<h3 class="title">Changes:</h3>'
        end_card = "</div></div>"

        cz_changes = self._changes(json_data, zone="cz")
        md_changes = self._changes(json_data, zone="md")

        if all(
            [len(cz_changes) == 0, len(md_changes) == 0, len(json_data["special"]) == 0]
        ):
            return card + '<h3 class="title">No Changes</h3>' + end_card

        if len(cz_changes) > 0:
            card += changes
            card += '<p class="description">'
            for change in cz_changes:
                card += change
            card = card[:-4] + "</p>"  # Retrait du dernier "<br>"
            changes = ""

        if len(md_changes) > 0:
            card += changes
            card += '<p class="description">'
            for change in md_changes:
                card += change
            card = card[:-4] + "</p>"  # Retrait du dernier "<br>"
            changes = ""

        if len(json_data["special"]) > 0:
            padding = " other-changes" if changes == "" else ""
            card += f'<h3 class="title{padding}">Other Changes:</h3>'
            card += f'<p class="description">{json_data["special"]}</p>'

        return card + end_card

    def compile_to_html(self, output_file):
        banlists_str_list = [
            self._create_html_card(self._json[date]) for date in self._dates
        ]

        with open(
            "mtgdc_banlist/static/banlist_html_header.html", "r", encoding="utf-8"
        ) as banlist_header_file:
            html_header = banlist_header_file.read()

        with open(
            "mtgdc_banlist/static/banlist_html_footer.html", "r", encoding="utf-8"
        ) as banlist_footer_file:
            html_footer = banlist_footer_file.read()

        output_file = "histo_banlists.html" if output_file == "" else output_file
        with open(output_file, "+w", encoding="utf-8") as banlist_file:
            banlist_file.truncate(0)
            banlist_file.seek(0)

            banlist_file.write(html_header)

            for line in banlists_str_list:
                banlist_file.write(line + "\n")

            banlist_file.write(html_footer)

    def is_banned(self, card, command_zone=False):
        if command_zone:
            return card in self.cz_bans

        return card in self.md_bans

    @property
    def md_bans(self):
        return self._current["banned_cards"]

    @property
    def cz_bans(self):
        return self._current["banned_commanders"]
