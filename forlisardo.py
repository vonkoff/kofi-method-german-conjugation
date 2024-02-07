from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import os
import re
import time
from .constants import templates

load_dotenv()
# SPEECH_KEY="6818a2214098a7e93b1d3da493ae" any of the keys you find in azure work
# SPEECH_REGION="eastus" you would choose another region
speech_key = os.environ.get("SPEECH_KEY")
speech_region = os.environ.get("SPEECH_REGION")


def synthesize_speech(text, filename):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )

    # https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechsynthesisoutputformat?view=azure-python
    # The lowest quality output is being used, but it suffices well and saves space.
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )

    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Prosody changes the speed at which the audio is said. I think .8 is about right
    # <voice name="de-DE-KillianNeural"> can be replaced by any of the other choices for a voice
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
        # For some reason I needed some delay to make this work. 1 second was fine and I kept 3 just in case
        time.sleep(3)
        return True
    else:
        print(f"Error synthesizing SSML: {ssml_string}")
        return False
