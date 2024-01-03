import uuid
import os
import genanki
from .constants import modal_verbs, tense_order, person_order


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
    tags = [f"tense:{tense}", f"verb:{verb}"]
    # print(f"Tags for verb {verb}: {tags}")


    if verb.endswith("en"):
        tags.append("ends_in_en")
    elif verb.endswith("ern"):
        tags.append("ends_in_ern")
    elif verb.endswith("eln"):
        tags.append("ends_in_eln")

    if subject is not None:
        if subject == "er":
            tags.append("person:er/sie/es")
        elif subject == "Sie":
            tags.append("person:sie/Sie")
        else:
            tags.append(f"person:{subject}")

    if verb in modal_verbs:
        tags.append("modal_verb")
    return tags


def order_notes(notes):
    custom_tense_order = []
    for str in tense_order:
        custom_tense_order.append(str.replace("tag:", ""))

    # Group notes by verb
    verb_groups = {}
    for note in notes:
        verb_tag = next(
            (tag for tag in note[0].tags if tag.startswith("verb:")), None)
        verb = verb_tag.split(":")[1] if verb_tag else None
        if verb:
            if verb not in verb_groups:
                verb_groups[verb] = []
            verb_groups[verb].append(note)

    # Sort function based on tense and person
    def sort_key(note):
        tense_tag = next(
            (tag for tag in note[0].tags if tag.startswith("tense:")), None)
        tense = tense_tag.split(":")[1] if tense_tag else None
        person_tag = next(
            (tag for tag in note[0].tags if tag.startswith("person:")), None)
        person = person_tag.split(":")[1] if person_tag else None
        tense_index = custom_tense_order.index(
            tense) if tense in custom_tense_order else len(custom_tense_order)
        person_index = person_order.index(
            person) if person in person_order else len(person_order)
        return tense_index, person_index

    # Sort within each verb group
    for verb, notes in verb_groups.items():
        notes.sort(key=sort_key)

    # Combine sorted notes, prioritizing modal verbs
    sorted_notes = []
    for verb in modal_verbs:
        if verb in verb_groups:
            sorted_notes.extend(verb_groups[verb])
            del verb_groups[verb]

    # Process remaining verbs
    for verb, notes in verb_groups.items():
        sorted_notes.extend(notes)

    return sorted_notes


def make_note(model, sentence, note, tags, form_audio_filename):

    # Extract tense name from tags
    tense_name = next((tag.replace("tense:", "") for tag in tags if "tense:" in tag), None)
    # Matching with audio file name
    template_audio = f"[sound:{tense_name}.mp3]" if tense_name else ""
    form_audio_filename = os.path.basename(form_audio_filename)
    form_audio = f"[sound:{form_audio_filename}]"

    print(f"Creating note. Sentence: {sentence}, Form Audio: {form_audio}, Template Audio: {template_audio}")



    my_note = genanki.Note(model=model, fields=[
        sentence, str(uuid.uuid4()), note, form_audio,template_audio
    ], tags=tags)

    # Metadata to order cars later
    metadata = {
        'is_modal': any(tag == "modal_verb" for tag in tags),
        'tense': tense_name,
        'person': next((tag for tag in tags if tag in person_order), None),
        'verb': next((tag for tag in tags if tag in "verb"), None)
    }

    return (my_note, metadata)

