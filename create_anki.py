import genanki
import os
from utils.speech import synthesize_speech, synthesize_template_speech, conjugated_audio
from utils.constants import kofi_css, templates, ge_deck_id, ge_deck_name
from utils.helpers import parse_verb_file, get_tags, make_note, order_notes


                        # # PRASENS, Konjunktiv II: Präteritum,
                        # # Indikativ: Präteritum
                        # word = person + " " + form
                        # sentence = get_sentence_template(tense, word, verb_name)
def get_sentence_template(tense, form, infinitive, person=""):
    person_with_space = f"{person} " if person else ""
    sentence_template = templates.get(tense, "").format(form, infinitive, person_with_space)
    if tense == "Infinitive":
        sentence = sentence_template.replace(
                '[...]', f'{{c1::{tense}}}')
    else:
        sentence = sentence_template.replace(
                '[...]', f'{{c1::{form}}}')
    return sentence


def create_anki_deck(verb_data):
    kofi_model = genanki.Model(
        model_id=391834738,
        name="Kofi German Conjugation Model",
        fields=[{"name": "Prompt"}, {"name": "UUID"}, {"name": "Notes"}, {
            "name": "Sound"}, {"name": "TemplateAudio"}],
        templates=[{
            "name": "Cloze",
            "qfmt": "{{cloze:Prompt}}<br>Template:{{TemplateAudio}}",
            "afmt": """{{cloze:Prompt}}<br><br>
            Pronuncation:{{Sound}}<br>
            <div class="back">
            <br /><br />
            &mdash;<br />
            Notes:{{Notes}}
            <br />
            &mdash;<br />

            {{#Tags}}
            <span class='tag_SECTION'>
            tags: <span class='tags'>{{Tags}}</span>
            </span>
            {{/Tags}}
            </div>"""
        }],
        css=kofi_css,
        model_type=genanki.Model.CLOZE
    )


    audio_files = synthesize_template_speech()
    print("Audio files to be included in the package:", audio_files)

    with open("results.txt", 'w+') as file:

        all_notes = []
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
                        audio = conjugated_audio(verb_name, form)
                        audio_files.append(audio)
                        all_notes.append(make_note(kofi_model, sentence, note, tags, audio))
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
                                audio = conjugated_audio(verb_name, imperativ)
                                audio_files.append(audio)
                                all_notes.append(make_note(kofi_model, sentence, note, tags, audio))
                                file.write(f"{sentence}\n")
                            continue

                        # PRASENS, Konjunktiv II: Präteritum,
                        # Indikativ: Präteritum
                        sentence = get_sentence_template(tense, form,
                                                         verb_name, person)
                        file.write(f"{sentence}\n")
                        tags = get_tags(tense, verb_name, person)
                        # Gesehen only 3rd person exists
                        if "–" in sentence:
                            continue

                        audio = conjugated_audio(verb_name, form)
                        audio_files.append(audio)
                        all_notes.append(make_note(kofi_model, sentence, note, tags, audio))
            # INFINITIVS
            # Get the third word which is the 3rd person form

            third_person_present = conjugations['Präsens'].split()[5]
            sentence = get_sentence_template("Infinitiv",
                                                      verb_name, third_person_present)
            file.write(f"{sentence}\n")
            tags = get_tags("Infinitiv", verb_name)
            audio = conjugated_audio(verb_name, verb_name)
            audio_files.append(audio)
            all_notes.append(make_note(kofi_model, sentence, note, tags, audio))

    ordered_notes = order_notes(all_notes)
    my_deck = genanki.Deck(deck_id=ge_deck_id, name=ge_deck_name)

    for note, _ in ordered_notes:
        my_deck.add_note(note)

    return my_deck, audio_files


# Main execution
verb_data = parse_verb_file("Konjugationen.txt")
anki_deck, audio_files = create_anki_deck(verb_data)
genanki.Package(anki_deck, media_files=audio_files).write_to_file('kofi_german_conjugation.apkg')
