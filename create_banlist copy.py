import glob
import json
import re
import textwrap
from datetime import datetime

from card_details import card_data


def clean_line(line):
    STRING_LIMIT = 100

    if len(line) > STRING_LIMIT:
        return "\n".join(textwrap.wrap(line, STRING_LIMIT))
    return line


def clean_rows(rows):
    good_rows = []
    for row in rows:
        good_rows.append(clean_line(row))
    return "\n".join(good_rows)


def get_header(header):
    rows = [row.strip() for row in header.splitlines()]
    return {
        "name": clean_line(rows[0]),
        "head_comment": clean_line(rows[1]),
    }


def get_general(general):
    rows = [row.strip() for row in general.splitlines()]
    tmp = {}
    for row in rows:
        try:
            section, change = row.split(":")
            if section not in tmp.keys():
                tmp[section] = []
            tmp[section].append(change)
        except ValueError:
            pass
    return tmp


def get_detailed(detailed):
    rows = [row.strip() for row in detailed.splitlines()]
    tmp = {}
    for row in rows:
        try:
            card, explanation = re.split(":", row, maxsplit=1)
            tmp[card] = card_data(card)
            tmp[card]["explanation"] = clean_line(explanation)
        except ValueError:
            pass

    return tmp


def handle_sections(sections):
    return (
        get_header(sections[0]),
        get_general(sections[1]),
        get_detailed(sections[2]),
    )


def format_banlist(date, entry):
    banlist = {
        "date": date,
        "entry": clean_rows([row.strip() for row in entry.splitlines()]),
    }

    sections = [row.strip() for row in entry.split("##")]
    header, general, detailed = handle_sections(sections)

    for k, v in header.items():
        banlist[k] = v

    for k, v in detailed.items():
        banlist[k] = v

    for k, v in general.items():
        banlist[k] = v
        if k == "Individual":
            for line in v:
                if "No change" not in line:
                    card = re.split(" is ", line, maxsplit=1)[0]
                    status = line[:-1].split(" ")[-1]
                    banlist[card]["status"] = status

    return banlist


banlists = []
for file in glob.glob("banlists" + "/*.txt"):
    with open(file, "r") as banlist_file:
        date = file.removeprefix("banlists/").removesuffix(".txt")
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        banlist_entry = banlist_file.read()
        banlists.append(format_banlist(date, banlist_entry))

sorted_banlists = sorted(banlists, key=lambda x: x["date"], reverse=True)

with open("banlist.json", "+w") as file:
    json.dump(sorted_banlists, file, ensure_ascii=False, indent=4)


def generate_toc(banlists):
    rows = []
    current_year = None
    for banlist in banlists:
        banlist_year = datetime.strptime(banlist["date"], "%Y-%m-%d").year
        if current_year != banlist_year:
            current_year = banlist_year
            rows.append(f'\n<h3><a id="Year{banlist_year}">{banlist_year}</a></h3>\n')
        rows.append(f"<a href=#{banlist['date']}>{banlist['name']}</a><br>")
    return "\n".join(rows) + "\n</center>\n<br/>\n"


with open("banlist.html", "+w") as banlist_file, open(
    "static/banlist_html_header.html", "r"
) as banlist_header_file, open(
    "static/banlist_html_footer.html", "r"
) as banlist_footer_file:
    banlist_file.truncate(0)
    banlist_file.seek(0)

    html_header = banlist_header_file.read()
    html_footer = banlist_footer_file.read()
    html_toc = generate_toc(sorted_banlists)
    banlist_file.write(html_header)
    banlist_file.write(html_toc)

    for banlist in sorted_banlists:
        banlist_file.write(f"<a id={banlist['date']} href=#>Top</a>\n")
        banlist_file.write("<hr><pre>\n")
        banlist_file.write(banlist["entry"])
        banlist_file.write("\n</pre>\n")

    banlist_file.write(html_footer)
