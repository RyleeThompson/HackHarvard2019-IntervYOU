from google.cloud import texttospeech
import os
import contextlib
import wave
from pydub import AudioSegment
import time

class TTSpeech:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
    
    def output(self, string, q, file_name = 'output.mp3'):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text = string)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(synthesis_input, voice, audio_config)
        
        # The response's audio_content is binary.
        with open(file_name, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)

        os.startfile(os.getcwd() + r'\output.mp3')
        q.put('done')
    
    def delay(self, q):
        audio = AudioSegment.from_file("output.mp3")
        audio.export(os.getcwd() + '\output.wav', format = 'wav')
        with contextlib.closing(wave.open(os.getcwd() + r'\output.wav', 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        time.sleep(duration + 0.2)
        q.put('done')
