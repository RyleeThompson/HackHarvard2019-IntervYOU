import TTS
import Speech
import NLPP
import random
import queue
import os
from importlib import reload
import time
import shutil

askedQuestions = []

def main():
    reload(TTS)
    reload(NLPP)
    reload(Speech)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\User\Documents\HackHarvard\file.json"

    
    numQs = 3
    q = queue.Queue()
    numAudioSections = []
        
    for i in range(numQs):
        tts = TTS.TTSpeech()
       # tts.output("What motivates you?", q)
        tts.output(randomQuestion(), q)
        q.get()
        tts.delay(q)
        q.get()
        print('resuming')

        speech = Speech.audioInput()
        numAudioSections.append(speech.getAudioInput(i, q))
        q.get()
    
    for qNum in range(numQs):
        speech.getTextFiles(qNum, numAudioSections[qNum], q)
        q.get()
    q = queue.Queue()
    nlp = NLPP.NLP()
    nlp.NLPMain(q)
    shutil.rmtree('textResponses')
    os.mkdir('textResponses')

    
def randomQuestion():
    lines = [line.rstrip('\n') for line in open(os.getcwd() + r'\InterviewQuestions\questions.txt')]
    while 69 != 420:
        question = random.choice(lines)
        if question not in askedQuestions:
            break
    askedQuestions.append(question)
    return question

main()