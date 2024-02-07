from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import os
import re
import time
from .constants import templates

load_dotenv()
speech_key = os.environ.get("SPEECH_KEY")
speech_region = os.environ.get("SPEECH_REGION")


def synthesize_speech(text, filename):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )

    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    ssml_string = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="de-DE">
        <voice name="de-DE-KillianNeural">
            <prosody rate=".8">{text}</prosody>
        </voice>
    </speak>
    """

    result = synthesizer.speak_ssml_async(ssml_string).get()
    print(result)

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Audio synthesized successfully: {filename}")
        time.sleep(3)
        return True
    else:
        print(f"Error synthesizing SSML: {ssml_string}")
        return False


def remove_html_and_special_symbols(text):
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)
    # Remove special symbols, but preserve German alphabets (ä, ö, ü, ß)
    text = re.sub(r"[^\w\säöüß]", "", text, flags=re.UNICODE)
    # Remove numbers
    text = re.sub(r"\d+", "", text)
    # Remove instances of 'c' followed by numbers
    text = re.sub(r"c\d+", "", text)
    # BLANKS for fill in?
    text = re.sub(r"\b[cC]\b", "BLANK", text)

    return text


def conjugated_audio(verb, form):
    folder_path = f"audio_files/{verb}"
    filename = os.path.join(folder_path, f"{form}.mp3")

    if not os.path.exists(filename):
        if synthesize_speech(form, filename):
            print("file create", filename)
            return filename
    else:
        print(f"File already exists, skipping: {filename}")
        return filename
    print("error creating speech file?")
    exit()


def synthesize_template_speech():
    audio_files = []
    folder_path = "audio_files/templates"
    cleaned_templates = {
        key: remove_html_and_special_symbols(value) for key, value in templates.items()
    }
    for tense, text in cleaned_templates.items():
        if tense == "Ind. Präteritum":
            tense = "Indikativ Präteritum"
        elif tense == "Sub. Präteritum":
            tense = "Konjunktiv II Präteritum"
        tense = tense.replace(" ", "_")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = os.path.join(folder_path, f"{tense}.mp3")
        if not os.path.exists(filename):
            print(f"Generating audio file: {filename}")
            if synthesize_speech(text, filename):
                audio_files.append(filename)
        else:
            print(f"File already exists, skipping: {filename}")
            audio_files.append(filename)
    return audio_files
