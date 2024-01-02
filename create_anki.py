import genanki
import os
from utils.speech import synthesize_speech, synthesize_template_speech
from utils.constants import kofi_css, templates
from utils.helpers import parse_verb_file, get_tags, make_card


def get_sentence_template(tense, form, infinitive):
    sentence_template = templates.get(tense, "").format(form, infinitive)
    if tense == "Infinitive":
        sentence = sentence_template.replace(
                '[...]', f'{{c1::{tense}}}')
    else:
        sentence = sentence_template.replace(
                '[...]', f'{{c1::{form}}}')
    return sentence


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
            "afmt": """{{cloze:Prompt}}<br>Notes:<br>{{Notes}}
            <br>{{Sound}}<br>Template Audio:{{TemplateAudio}}"""
        }],
        css=kofi_css,
        model_type=genanki.Model.CLOZE
    )

    audio_files = synthesize_template_speech()

    with open("results.txt", 'w+') as file:

        for verb_name, note, conjugations in verb_data:
            word_folder = os.path.join("audio_files", verb_name)
            os.makedirs(word_folder, exist_ok=True)

            file.write(f"VERB: {verb_name}\n")
            file.write(f"NOTE: {note}\n")
            for tense, conjs in conjugations.items():

                # PARTIZIP I and PARTIZIP II
                if tense in ["Partizip I", "Partizip II"]:
                    # Split the conjugations into individual forms
                    forms = conjs.split()

                    for form in forms:
                        form = form.translate({ord(i): None for i in '!,'})
                        sentence = get_sentence_template(tense,
                                                         form, verb_name)
                        file.write(f"{sentence}\n")
                        tags = get_tags(tense, verb_name)
                        make_card(my_deck, kofi_model, sentence, note, tags)
                else:

                    forms = conjs.split()
                    for i in range(0, len(forms), 2):
                        person = forms[i].translate({ord(i): None for i in '!,'})
                        form = forms[i+1].translate({ord(i): None for i in '!,'})
                        # IMPERATIVS
                        if tense == "Imperativs":
                            singular = person
                            plural = form
                            for i, imperativ in enumerate([singular, plural]):
                                sentence = get_sentence_template(tense,imperativ, verb_name)
                                subject = "du" if i == 0 else "ihr/Sie"
                                tags = get_tags(tense, verb_name, subject)
                                make_card(my_deck, kofi_model, sentence, note, tags)
                                file.write(f"{sentence}\n")
                            continue

                        # PRASENS, Konjunktiv II: Präteritum,
                        # Indikativ: Präteritum
                        word = person + " " + form
                        sentence = get_sentence_template(tense, word, verb_name)
                        file.write(f"{sentence}\n")
                        tags = get_tags(tense, verb_name, person)
                        make_card(my_deck, kofi_model, sentence, note, tags)
            # INFINITIVS
            # Get the third word which is the 3rd person form
            third_person_present = conjugations['Präsens'].split()[5]
            sentence = get_sentence_template("Infinitiv",
                                                      verb_name, third_person_present)
            file.write(f"{sentence}\n")
            tags = get_tags("Infinitiv", verb_name)
            make_card(my_deck, kofi_model, sentence, note, tags)

    return my_deck, audio_files


# Main execution
verb_data = parse_verb_file("Konjugationen.txt")
anki_deck, media_files = create_anki_deck(verb_data)
genanki.Package(anki_deck, media_files=media_files).write_to_file(
    'kofi_german_conjugation.apkg')
