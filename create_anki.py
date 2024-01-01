import genanki
from random import seed
from random import randint
import os
import uuid
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from constants import kofi_css

load_dotenv()
speech_key = os.environ.get('SPEECH_KEY')
speech_region = os.environ.get('SPEECH_REGION')


    # Mujer, por favor,<br>¡ no <span class="de_verb">
    # {{c1::seas::…ser…}}</span> <span class="sp_hint">(así)</span> !<br><br><span class="tu_vos_hint">(tú/vos)</span>
templates = {
    "Präsens": "⊙ Jetzt gerade, ⊙<br><span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> über die Vergangenheit.",
    "Ind. Präteritum": "← Zu dieser Zeit, oft, ←<br><span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> gestern über die Vergangenheit",
    "Sub. Präteritum": "↫ Es war überraschend, dass ↫<br><span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> gestern über die Vergangenheit",
    "Imperativs": "Bitte, Mann,<br><span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> jetzt!",
    "Partizip I": "Ich sah den Mann, während er über die Vergangenheit <span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span> ging",
    "Partizip II": "Das Objekt wurde <span class=\"de_verb\">{{{{c1::{0}::{1}}}}}</span>",
    "Infinitiv": "Das Verb in<br><span class=\"cloze_hilite\">er {1}</span><br>ist zu <span class=\"de_verb\">{{{{c1::{0}}}}}</span>"
}


def synthesize_speech(text, filename):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = 'de-DE-KillianNeural'

    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)

    ssml_string = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="de-DE">
        <voice name="de-DE-KillianNeural">
            <prosody rate="1">{text}</prosody>
        </voice>
    </speak>
    """

    result = synthesizer.speak_ssml_async(ssml_string).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Audio synthesized successfully: {filename}")
    else:
        print(f"Error synthesizing SSML: {ssml_string}")


def parse_verb_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting by "####" to get each verb block
    verbs = content.split("####")[1:]
    verb_data = []

    for verb in verbs:
        lines = verb.strip().split("\n")
        if lines:
            # Extract verb name from the first line, assuming it's formatted as 'zu [verb]'
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

def get_sentence_template(tense, form, infinitive):
    return templates.get(tense, "").format(form, infinitive)


def synthesize_template_speech():
    audio_files = []
    for tense, text in templates.items():
        filename = os.path.join("audio_files/templates", f"{tense}.mp3")
        # Only synthesize if file doesn't exist
        if not os.path.exists(filename):
            if synthesize_speech(text, filename):
                audio_files.append(filename)
    return audio_files


def create_anki_deck(verb_data):
    my_deck = genanki.Deck(deck_id=391834738, name='KOFI German')

    kofi_model = genanki.Model(
        model_id=391834738,
        name="Kofi German Conjugation Model",
        fields=[{"name": "UUID"}, {"name": "Prompt"}, {"name": "Notes"}, {
            "name": "Sound"}, {"name": "TemplateAudio"}],
        templates=[{
            "name": "Card 1",
            "qfmt": "{{cloze:Prompt}}<br>{{Sound}}",
            "afmt": "{{cloze:Prompt}}<br>Notes:<br>{{Notes}}<br>{{Sound}}<br>Template Audio:{{TemplateAudio}}"
        }],
        css=kofi_css
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
                # Check for tenses that don't follow the standard pronoun-verb pair format
                # print(tense, conjs)
                if tense in ["Partizip I", "Partizip II"]:
                    # Split the conjugations into individual forms
                    forms = conjs.split()

                    for form in forms:
                        form = form.translate({ord(i): None for i in '!,'})
                        sentence_template = get_sentence_template(tense,form,verb_name)
                        sentence = sentence_template.replace(
                            '[...]', f'{{c1::{form}}}')

                        file.write(f"{sentence}\n")
                        my_note = genanki.Note(model=kofi_model, fields=[
                            str(uuid.uuid4(
                            )), sentence, note, "sound", "template_audio"]
                                               )
                        my_deck.add_note(my_note)

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
                                file.write(f"{sentence}\n")
                            continue

                        word = person + " " + form
                        sentence_template = get_sentence_template(tense, word, verb_name)
                        sentence = sentence_template.replace(
                            '[...]', f'{{c1::{word}}}')

                        file.write(f"{sentence}\n")
                        my_note = genanki.Note(model=kofi_model, fields=[
                            str(uuid.uuid4(
                            )), sentence, note, "sound", "template_audio"]
                                               )
                        my_deck.add_note(my_note)

            third_person_present = conjugations['Präsens'].split()[5]  # Get the third word which is the 3rd person form
            sentence_template = get_sentence_template("Infinitiv", verb_name, third_person_present)
            sentence = sentence_template.replace(
                '[...]', f'{{c1::{verb_name}}}')
            file.write(f"{sentence}\n")
            my_note = genanki.Note(model=kofi_model, fields=[
                str(uuid.uuid4(
                )), sentence, note, "sound", "template_audio"]
                                   )
            my_deck.add_note(my_note)

                    # print(
                    #     f"Generated text for verb '{verb_name}', tense '{tense}', form '{form}': {sentence}")

                    # audio_filename = os.path.join(
                    #     word_folder, f"{verb_name}_{tense}_{i}.mp3")
                    # if synthesize_speech(sentence, audio_filename):
                    #     audio_files.append(audio_filename)

                    # template_audio_filename = f"audio_files/templates/{tense}.mp3"
                    # my_note = genanki.Note(model=kofi_model, fields=[
                    #     str(uuid.uuid4(
                    #     )), sentence, note, f"[sound:{os.path.basename(audio_filename)}]", f"[sound:{os.path.basename(template_audio_filename)}]"
                    # ])
                    # my_deck.add_note(my_note)

    return my_deck, audio_files


# Main execution
verb_data = parse_verb_file("Konjugationen.txt")
anki_deck, media_files = create_anki_deck(verb_data)
genanki.Package(anki_deck, media_files=media_files).write_to_file(
    'kofi_german_conjugation.apkg')
