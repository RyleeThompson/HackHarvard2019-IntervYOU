import wave
import pyaudio
import numpy as np
from pydub import AudioSegment
import io
import os
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import threading

def getTextFiles(numQuestions):
    # Instantiates a client
    client = speech.SpeechClient()

    for i in range(numQuestions):
        # The name of the audio file to transcribe
        file_name = os.path.join(
            os.getcwd(),
            'Answer' + str(i + 1) + '.flac')
        
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            audio_channel_count = 2,
            language_code='en-US')

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        textData = str()
        for result in response.results:
            textData += result.alternatives[0].transcript
            textData += '.'
        with io.open('answer' + str(i + 1) + '.txt', 'w+') as text_file:
            text_file.write(textData)
