import genanki
from random import seed
from random import randint
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from constants import kofi_css


def synthesize_speech(text, filename):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = 'de-DE-KatjaNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Error synthesizing text: {text}")
        return False
    return True


load_dotenv()
speech_key = os.environ.get('SPEECH_KEY')
speech_region = os.environ.get('SPEECH_REGION')

seed(1)
for _ in range(10):
    rval = randint(0, 9)

my_deck = genanki.Deck(
    # Remove for user later
    deck_id=1239481293,
    name='KOFI German'
)

# Define the model
kofi_model = genanki.Model(
    # Remove for user later
    model_id=391834738,  # Replace with your unique model ID
    name="Kofi German Conjugation Model",
    fields=[
        {"name": "UUID"},
        {"name": "Prompt"},
        {"name": "Similar"},
        {"name": "Notes"}
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": """
                {{cloze:Prompt}}
            """,  # Front of the card
            "afmt": """
                {{cloze:Prompt}}<br>
                <hr id="answer">
                {{Similar}}<br>
                <hr>
                Notes:<br>
                {{Notes}}
            """  # Back of the card
        }
    ],
    css=kofi_css
)

words = {
    "laufen": ["Ich laufe", "Du läufst"]
}
audio_files = []

for word, conjugations in words.items():
    word_folder = f"audio_files/{word}"
    os.makedirs(word_folder, exist_ok=True)

    for i, text in enumerate(conjugations):
        # audio_filename = os.path.join(word_folder, f"{word}_{i}.mp3")
        # if synthesize_speech(text, audio_filename):
        #     audio_files.append(audio_filename)
        my_note = genanki.Note(model=kofi_model,
                               fields=[
                                   # UUID
                                   "8ac5-4121-856c-1233ba44a",
                                   # Prompt
                                   "Das Verb in<br><span class=\"cloze_hilite\">es ist</span><br>ist zu <span class=\"sp_verb\">{{c1::sein}}</span>",
                                   # Similar
                                   "",
                                   #    "<br><span class=\"alt_conj\">buscábamos</span>←<span class=\"alt_inf\"><a href=\"https://dle.rae.es/buscar?m=form#conjugacion\">buscar</a></span><br><span class=\"alt_conj\">cambiábamos</span>←<span class=\"alt_inf\"><a href=\"https://dle.rae.es/cambiar?m=form#conjugacion\">cambiar</a></span><br><span class=\"alt_conj\">causábamos</span>←<span class=\"alt_inf\"><a href=\"https://dle.rae.es/causar?m=form#conjugacion\">causar</a></span><br><span class=\"alt_conj\">llevábamos</span>←<span class=\"alt_inf\"><a href=\"https://dle.rae.es/llevar?m=form#conjugacion\">llevar</a></span><br><span class=\"alt_conj\">dejábamos</span>←<span class=\"alt_inf\"><a href=\"https://dle.rae.es/dejar?m=form#conjugacion\">dejar</a></span><br><span class=\"alt_conj\">quedábamos</span>←<span class=\"alt_inf\"><a href=\"https://dle.rae.es/quedar?m=form#conjugacion\">quedar</a></span>",  # Similar
                                   # Notes
                                   "",
                                   #    "<span class=\"SECTION_family\"><br><span class=\"dle_conj\"><a href=\"https://dle.rae.es/hablar?m=form#conjugacion\">hablar</a></span> is a <span class=\"note_feature\">regular verb in -ar</span></span>"  # Notes
                               ],
                               tags=["test"]
                               )
        my_deck.add_note(my_note)

genanki.Package(my_deck, media_files=audio_files).write_to_file(
    'kofi_german_conjugation.apkg')
