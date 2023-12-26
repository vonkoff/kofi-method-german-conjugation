import genanki
from random import seed
from random import randint
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk


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
    deck_id=rval,
    name='KOFI German Conjugation'
)

my_template = genanki.Model(
    model_id=rval,
    name='FAKE DRAFT Model w/ Audio',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'MyMedia'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br>{{MyMedia}}',
        },
    ])

words = {
    "laufen": ["Ich laufe", "Du läufst"]
}
audio_files = []

for word, conjugations in words.items():
    word_folder = f"audio_files/{word}"
    os.makedirs(word_folder, exist_ok=True)

    for i, text in enumerate(conjugations):
        audio_filename = os.path.join(word_folder, f"{word}_{i}.mp3")
        if synthesize_speech(text, audio_filename):
            audio_files.append(audio_filename)
            my_note = genanki.Note(model=my_template,
                                   fields=[text, "Translation here",
                                           f'[sound:{word}_{i}.mp3]'],
                                   #    tags=["tags"]
                                   )
            my_deck.add_note(my_note)

genanki.Package(my_deck, media_files=audio_files).write_to_file(
    'kofi_german_conjugation.apkg')
