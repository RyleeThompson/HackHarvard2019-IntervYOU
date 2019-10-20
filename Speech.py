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
import queue
import time

#Gets and saves the answer to a question
import pyaudio
import numpy as np
import wave
from pydub import AudioSegment
import shutil

class audioInput:
    def getAudioAnswer(self, answer, q, CHUNK = 2048, FORMAT = pyaudio.paInt16, CHANNELS = 2, RATE = 48000, RECORD_SECONDS = 1000):
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []
        means = np.array([])
        counter = 0
        started = 0
        part = 1
        max_mean = 500

        for j in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            #read data from mic
            data = stream.read(CHUNK)

            #write data to notUsed -> required to get data in array form
            wf = wave.open(r'audio\notUsed' + str(j) + '.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join([data, data]))
            wf.close()

            #Get data in array
            audio = AudioSegment.from_file(r'audio\notUsed' + str(j) + '.wav')
            x = np.abs(audio.get_array_of_samples())/2
            mean = np.mean(x)
            #print(mean)
            means = np.append(means, mean)

            #Only append data if the interviewee has begun answering
            if started == 0 and mean > max_mean:
                started = 1
                j = 0
            if j % 702 == 0 and j != 0 and started == 1:
                wf = wave.open(r'audioResponses\answer' + str(answer) + 'pt' + str(part) + '.flac', 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                frames = []
                part += 1
            if started == 1:
                frames.append(data)
            means = np.append(means, np.mean(x))
            #print(means)
            if mean <= max_mean and started == 1:
                counter += 1
            else:
                counter = 0
            if counter >= 40:
                break

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf1 = wave.open(r'audioResponses\answer' + str(answer) + 'pt' + str(part) + '.flac', 'wb')
        wf1.setnchannels(CHANNELS)
        wf1.setsampwidth(p.get_sample_size(FORMAT))
        wf1.setframerate(RATE)
        wf1.writeframes(b''.join(frames))
        wf1.close()
        shutil.rmtree('audio')
        q.put('Done')
       # print(np.mean(means))
        return part

    #Gets the audio input for a given number of questions
    def getAudioInput(self, qNum, q):
        Rate = 48000
        self.makeDirectory()
        Length = self.getAudioAnswer(qNum + 1, q, RATE = Rate)
        q.get()
        q.put('Done')
        return Length

    def makeDirectory(self):
        try:
            os.mkdir('audio')
        except:
            pass
        try:
            os.mkdir('textResponses')
        except:
            pass
        try:
            os.mkdir('audioResponses')
        except:
            pass
    def getTextFiles(self, questionNum, lens, q):
        # Instantiates a client
        client = speech.SpeechClient()

        for j in range(lens):
            # The name of the audio file to transcribe
            file_name = os.getcwd() + r'\audioResponses\answer' + str(questionNum + 1) + 'pt' + str(j + 1) + '.flac'
            
            with io.open(file_name, 'rb') as audio_file:
                content = audio_file.read()
                audio = types.RecognitionAudio(content=content)
                
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                audio_channel_count = 2,
                language_code='en-US')
            
            # Detects speech in the audio file
            response = client.recognize(config, audio)
            
            textData = str()
            for result in response.results:
                textData += result.alternatives[0].transcript
                textData += '.'
            with io.open(os.getcwd() + r'\textResponses\answer' + str(questionNum + 1) + '.txt', 'w+') as text_file:
                text_file.write(textData)
        q.put('Done')

    def clean(self):
        shutil.rmtree('audioResponses')
        shutil.rmtree('textResponses')
    def mainAudio(self, q2):
        q = queue.Queue()
        lens = self.getAudioInput(2, q)
        q.get()
        self.getTextFiles(2, lens, q)
        q.get()
        q2.put('done')
        #self.clean()
        #q.get()
