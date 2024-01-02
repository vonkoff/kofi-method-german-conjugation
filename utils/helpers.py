import uuid
import genanki


def parse_verb_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting by "####" to get each verb block
    verbs = content.split("####")[1:]
    verb_data = []

    for verb in verbs:
        lines = verb.strip().split("\n")
        if lines:
            # Extract verb name from the first line,
            # assuming it's formatted as 'zu [verb]'
            verb_name = lines[0].strip().split('zu ')[-1].strip()

            note = ""
            conjugations = {}

            for line in lines[1:]:
                if line.startswith("Note:"):
                    note = line.replace("Note: ", "").strip()
                elif ':' in line:
                    tense, conj = line.split(":", 1)
                    conjugations[tense.strip()] = conj.strip()

            verb_data.append((verb_name, note, conjugations))
    return verb_data


def get_tags(tense, verb, subject=None):

    if tense == "Ind. Präteritum":
        tense = "Indikativ Präteritum"
    elif tense == "Sub. Präteritum":
        tense = "Konjunktiv II Präteritum"
    tense = tense.replace(" ", "_")
    tags = [f"tag:{tense}", f"tag:{verb}"]

    if verb.endswith("en"):
        tags.append("tag:ends_in_en")
    elif verb.endswith("ern"):
        tags.append("tag:ends_in_ern")
    elif verb.endswith("eln"):
        tags.append("tag:ends_in_eln")

    if subject is not None:
        tags.append(f"tag:{subject}")

    modal_verbs = ["können", "müssen", "wollen", "sollen", "dürfen", "mögen"]

    if verb in modal_verbs:
        tags.append("tag:modal_verb")
    return tags


def make_card(deck, model, sentence, note, tags,
              sound=None, template_audio=None):
    my_note = genanki.Note(model=model, fields=[
        sentence, str(uuid.uuid4()), note, "sound", "template_audio"],
                           tags=tags)
    deck.add_note(my_note)
