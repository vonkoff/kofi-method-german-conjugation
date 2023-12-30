import requests
from bs4 import BeautifulSoup
import re
import time
import random
import os


def url_umlauts(word):
    """ German umlauts and sharp S. Replace so it can be used in url """
    return word.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')


def clean_text(input_text):
    """ Remove content within parentheses (including parentheses) and digits """
    return re.sub(r"\s?\([^)]*\)|\d", "", input_text)


def appendCon(arr, table, skip=False, ppronoun=False):
    pronouns = ["ich", "du", "er/sie/es", "wir", "ihr", "sie"]
    ul_tag = table.find("ul", {"class": "accordion__list content-column"})
    li_tags = ul_tag.find_all("li", {"class": "accordion__item"})

    for i, li_tag in enumerate(li_tags):
        if i != 0 or skip:
            litext = clean_text(li_tag.text)
            words = litext.split()
            selected_word = words[-1] if ppronoun else words[0]

            if ppronoun:
                third_pro = random.choice(
                    ['er', 'sie', 'es']) if pronouns[i - 1] == "er/sie/es" else pronouns[i - 1]
                arr.append(third_pro + " " + selected_word)
            else:
                arr.append(litext if "zu" in words else selected_word)


def write_conjugations(f, conjugations, tense):
    if any(conj == "–" for conj in conjugations):
        f.writelines([tense, ":\n"])
    else:
        f.writelines([tense, ": ", " ".join(conjugations), "\n"])


def scrape_strong_verbs():
    url = "https://jakubmarian.com/list-of-irregular-strong-german-verbs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all(
        'table', {"class": "bordered german-verbs zoomed"})[1]
    rows = table.find_all('tr')

    with open("StarkeVerben.txt", "w") as f:
        for row in rows:
            verbs = row.find_all('td', {"class": "verb"})
            notes = row.find_all('td', {"class": "note"})
            for verb, note in zip(verbs, notes):
                verb_text = verb.contents[0]
                note_text = note.get_text(strip=True)
                f.writelines(["Verb: ", verb_text, "\n",
                             "Note: ", note_text, "\n"])


# Check if "StarkeVerben.txt" exists, if not, scrape strong verbs
if not os.path.exists("StarkeVerben.txt"):
    scrape_strong_verbs()

# Main script starts here
user_agent = 'starkesVerbScraper/1.0 (ivanl@fastmail.com)'
headers = {'User-Agent': user_agent}
verbs = []

with open("StarkeVerben.txt", "r") as fi:
    verb, note = None, None
    for line in fi:
        if line.startswith('Verb:'):
            verb = line.split(':')[1].strip()
        elif line.startswith('Note:'):
            note = line.split(':', 1)[1].strip() if ':' in line else ""
            verbs.append([verb, note])
            verb, note = None, None

for verb_info in verbs:
    verb = verb_info[0]
    note = verb_info[1]
    time.sleep(5)
    url = "https://www.duden.de"
    search = f"/suchen/dudenonline/{verb}"
    url_search = url + search
    response = requests.get(url_search)

    if response.status_code == 404:
        with open("missing_verb.txt", "a") as missing_file:
            missing_file.write(verb + "\n")
        continue
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    sections = soup.findAll('section', {"class": "vignette"})

    f = open("Konjugationen.txt", "a")
    print(f"################################################ VERB - {verb}")
    for section in sections:
        if "starkes" or "unregelmäßiges" in section.text:
            ###!
            print(section)
            a = section.find('a', {"class": "vignette__link"})
            ahref = a['href']
            ahref = ahref.replace("rechtschreibung", "konjugation")
            url_search = url + ahref
            # check if corr verb
            corr_verb = url_search.split("konjugation/", 1)[1]
            ###!
            print(corr_verb)
            if corr_verb != url_umlauts(verb):
                continue
            print(url_search)
            response = requests.get(url_search)

            # missing words like gelingen and schaffen from duden.de for conjugation
            # Will be manually inputted with conjugation
            if response.status_code == 404:
                with open("missing_verb.txt", "a") as missing_file:
                    missing_file.write(verb + "\n")
                continue  # Skip to the next verb
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            tables = soup.find_all('div', {"class", "accordion-table"})

            prasens = []
            prateritums = []
            prateritums_sub = []
            imperativs = []
            infinitivs = []
            partizipIs = []
            partizipIIs = []
            for table in tables:
                if "Präsens" in table.text and not prasens:
                    appendCon(prasens, table, ppronoun=True)
                # Subjunctive prat. goes first. Since indik needs to not be full. Shows up 2nd
                if "Präteritum" in table.text and prateritums and not prateritums_sub:
                    appendCon(prateritums_sub, table, ppronoun=True)
                if "Präteritum" in table.text and not prateritums:
                    appendCon(prateritums, table, ppronoun=True)
                if "Person Singular [du]" in table.text and not imperativs:
                    #! Need to add in infinitive + wir/sie
                    #! Also add in
                    appendCon(imperativs, table, True)
                if "Infinitiv" in table.text and not infinitivs:
                    appendCon(infinitivs, table)
                if "Partizip I" in table.text and not partizipIs:
                    appendCon(partizipIs, table)
                if "Partizip II" in table.text and not partizipIIs:
                    appendCon(partizipIIs, table)

            # print(prasens)
            # print(prateritums)
            # print(imperativs)
            # print(infinitivs)
            # print(partizipIIs, partizipIs)

            for i in range(0, 7):
                conjugations = ["", prasens, prateritums, prateritums_sub,
                                imperativs, partizipIs, partizipIIs]
                if i == 0:
                    # print(" ".join(infinitivs), f"count -> {i}")
                    f.writelines(
                        ['#### ', " ".join(infinitivs), " ####", "\n"])
                    f.writelines(["Note: ", note, "\n"])  # Include the note
                else:
                    tense = ""
                    if conjugations[i] == prasens:
                        tense = "Präsens"
                    elif conjugations[i] == prateritums:
                        tense = "Ind. Präteritum"
                    elif conjugations[i] == prateritums_sub:
                        tense = "Sub. Präteritum"
                    elif conjugations[i] == imperativs:
                        tense = "Imperativs"
                    elif conjugations[i] == partizipIs:
                        tense = "Partizip I"
                    elif conjugations[i] == partizipIIs:
                        tense = "Partizip II"

                    # print(conjugations[i], "normal print")
                    # print(" ".join(conjugations[i]), f"count -> {i}")
                    write_conjugations(f, conjugations[i], tense)

    f.close()
