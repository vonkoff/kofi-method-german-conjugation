from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import os
from .constants import templates

load_dotenv()
speech_key = os.environ.get('SPEECH_KEY')
speech_region = os.environ.get('SPEECH_REGION')


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


def synthesize_template_speech():
    audio_files = []
    for tense, text in templates.items():
        filename = os.path.join("audio_files/templates", f"{tense}.mp3")
        # Only synthesize if file doesn't exist
        if not os.path.exists(filename):
            if synthesize_speech(text, filename):
                audio_files.append(filename)
    return audio_files
