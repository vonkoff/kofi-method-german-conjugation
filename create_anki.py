import genanki
from random import seed
from random import randint
import uuid
import os
from utils.speech import synthesize_speech, synthesize_template_speech
from utils.constants import kofi_css, templates
from utils.helpers import parse_verb_file, get_tags, make_card

def get_sentence_template(tense, form, infinitive):
    return templates.get(tense, "").format(form, infinitive)


def create_anki_deck(verb_data):
    my_deck = genanki.Deck(deck_id=391834738, name='KOFI German')

    kofi_model = genanki.Model(
        model_id=391834738,
        name="Kofi German Conjugation Model",
        fields=[{"name": "Prompt"}, {"name": "UUID"}, {"name": "Notes"}, {
            "name": "Sound"}, {"name": "TemplateAudio"}],
        templates=[{
            "name": "Cloze",
            "qfmt": "{{cloze:Prompt}}<br>{{Sound}}",
            "afmt": "{{cloze:Prompt}}<br>Notes:<br>{{Notes}}<br>{{Sound}}<br>Template Audio:{{TemplateAudio}}"
        }],
        css=kofi_css,
        model_type=genanki.Model.CLOZE
    )

    audio_files = synthesize_template_speech()

    with open("results.txt", 'w+') as file:

        for verb_name, note, conjugations in verb_data:
            word_folder = os.path.join("audio_files", verb_name)
            os.makedirs(word_folder, exist_ok=True)

            # file.write(f"{verb_name}\n{note}\n{conjugations}")
            file.write(f"VERB: {verb_name}\n")
            file.write(f"NOTE: {note}\n")
            print(conjugations.items())
            for tense, conjs in conjugations.items():

                if tense in ["Partizip I", "Partizip II"]:
                    # Split the conjugations into individual forms
                    forms = conjs.split()

                    for form in forms:
                        form = form.translate({ord(i): None for i in '!,'})
                        sentence_template = get_sentence_template(tense,form,verb_name)
                        sentence = sentence_template.replace(
                            '[...]', f'{{c1::{form}}}')

                        file.write(f"{sentence}\n")
                        tags = get_tags(tense, verb_name)
                        make_card(my_deck, kofi_model, sentence, note, tags)
                else:
                    forms = conjs.split()
                    print(f"forms other: {forms}")

                    for i in range(0, len(forms), 2):
                        person = forms[i].translate({ord(i): None for i in '!,'})
                        form = forms[i+1].translate({ord(i): None for i in '!,'})
                        if tense == "Imperativs":
                            singular = forms[i].translate({ord(i): None for i in '!,'})
                            plural = forms[i+1].translate({ord(i): None for i in '!,'})
                            for i, imperativ in enumerate([singular, plural]):
                                sentence_template = get_sentence_template(tense, imperativ, verb_name)
                                sentence = sentence_template.replace(
                                    '[...]', f'{{c1::{imperativ}}}')

                                subject = "du" if i == 0 else "ihr/Sie"
                                tags = get_tags(tense, verb_name, subject)
                                make_card(my_deck, kofi_model, sentence, note, tags)
                                file.write(f"{sentence}\n")
                            continue

                        word = person + " " + form
                        sentence_template = get_sentence_template(tense, word, verb_name)
                        sentence = sentence_template.replace(
                            '[...]', f'{{c1::{word}}}')

                        file.write(f"{sentence}\n")
                        tags = get_tags(tense, verb_name, person)
                        print(tags, "PRASENS")
                        make_card(my_deck, kofi_model, sentence, note, tags)

            # INFINITIVE
            third_person_present = conjugations['Präsens'].split()[5]  # Get the third word which is the 3rd person form
            sentence_template = get_sentence_template("Infinitiv", verb_name, third_person_present)
            sentence = sentence_template.replace(
                '[...]', f'{{c1::{verb_name}}}')
            file.write(f"{sentence}\n")
            tags = get_tags("Infinitiv", verb_name)
            make_card(my_deck, kofi_model, sentence, note, tags)

    return my_deck, audio_files


# Main execution
verb_data = parse_verb_file("Konjugationen.txt")
anki_deck, media_files = create_anki_deck(verb_data)
genanki.Package(anki_deck, media_files=media_files).write_to_file(
    'kofi_german_conjugation.apkg')
