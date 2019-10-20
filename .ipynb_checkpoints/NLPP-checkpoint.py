from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import numpy as np
import os
import inflect

class NLP:
    def __init__(self):
        self.client = language.LanguageServiceClient()
    def NLPMain(self, q):    
        positive = ['research','best','attention','effort']
        negative = open(os.getcwd() + r"\lexicons\negative-words.txt","r").read().split('\n')
        pContainer = []
        pHold = []
        nContainer = []
        nHold = []
        strMaster = ""
        listMaster = []

        sentimentMaster = self.sentimentAnalysis(self.textScraper(os.getcwd() + r'\textResponses'))

        for i in range(len(positive)):
            pInstances = (self.entityCount(sentimentMaster[0],positive[i]))
            pContainer.append(pInstances)
            if pInstances != 0:
                #print("The word <{}> was used {} times.".format(positive[i],pInstances))
                pHold.append(positive[i])

        for i in range(len(negative)):
            nInstances = (self.entityCount(sentimentMaster[0],negative[i]))
            nContainer.append(nInstances)
            if nInstances !=0:
                #print("The word <{}> was used {} times.".format(negative[i],nInstances))
                nHold.append(negative[i])

        strMaster = ''.join(map(str,sentimentMaster[0]))
        listMaster = list(strMaster.split(" "))
        #print(np.argsort(nContainer))
        #print(np.argsort(sentimentMaster[1]))
        #print(sum(nContainer))
        #print(listMaster)
        #print(len(listMaster))

        nRatio = sum(nContainer)/len(listMaster)

        print(self.nRatioTransform(nRatio))

        if nRatio >.2:
                print("{}".format(nHold))
        q.put('done')


    #Counts the frequency of target words from a text database within user response
    def entityCount(self, response,entity):
        tempResponse = ','.join(response)
        if entity =='':
            instances = 0;
        else:
            instances = tempResponse.count(entity)
        return instances

    # Sentimental Analysis of each response via Google Cloud NLP method 
    def sentimentAnalysis(self, text):
        p = inflect.engine()
        sentimentContainer = []
        respList = []
        for i in range(len(text)):
            document = types.Document( 
            content = open(text[i],"r").read(),
            type = enums.Document.Type.PLAIN_TEXT)

            sentiment = self.client.analyze_sentiment(document=document).document_sentiment
            sentimentContainer.append(sentiment.score)

            tempStr = open(text[i],"r").read()
            respList.append(tempStr)

            y = i + 1
            print('Your {} response produced the following score'.format(p.ordinal(y)))
            print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

            qualScore = self.scoreTransform(sentiment.score)
            #qualMag = magTransform(sentiment.magnitude)
            print(qualScore)

        return respList, sentimentContainer, qualScore

    def nRatioTransform(self, nRatio):
        print("Your responses contained {:.0%} negative bias words.".format(nRatio))
        if nRatio <.001: 
            nRatioEval = "Your responses contained negligible amounts of negative bias words"
        elif nRatio <.1:
            nRatioEval = "Your responses contained an acceptable amount of negative bias words."
        elif nRatio <.2:
            nRatioEval = "Please reconsider the use of the following word choices:" 
        else:
            nRatioEval = "The following words/phrase will have a negative impact during the interview environment:"

        return nRatioEval

    # Convert quantitative metrics to user friendly feedback strings
    def scoreTransform(self, score):
        if score >0.8: 
            scoreEval = "This was a very positive response\n"
        elif score >0.4:
            scoreEval = "This was a positive response\n"
        elif score >0:
            scoreEval = "This was a somewhat positive response\n"
        elif score ==0: 
            scoreEval = "This is a neutral response\n"
        elif score <-0.6:
            scoreEval = "This is a very negative response\n"
        else:
            scoreEval = "This was a negative response\n"

        return scoreEval

    # Loading in all text files from a target directory
    def textScraper(self, path):
        text = []

        for file in os.listdir(path):
            if file.endswith(".txt"):
                temp = os.path.join(path,file)
                text.append(temp)
        return(text)
