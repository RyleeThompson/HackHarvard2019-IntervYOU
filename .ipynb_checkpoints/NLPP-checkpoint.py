from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import numpy as np
import os
import inflect

sentScore = 0

class NLP:
    def __init__(self):
        self.client = language.LanguageServiceClient()
    def NLPMain(self, q):    
       # positive = ['research','best', 'attention', 'effort']
        fillerOneWord = ['like', 'totally', 'basically', 'seriously', 'actually', 'just', 'literally']
        fillTwoWords = ['youknow', 'yousee', 'Imean', 'orsomething', 'sortof', 'kindof', 'okayso', 'Ijust']
        fillTwoWords2 = ['you know', 'you see', 'I mean', 'or something', 'sort of', 'kind of', 'okay so', 'I just']
        negative = open(os.getcwd() + r"\lexicons\negative-words.txt","r").read().split('\n')
        #assertives = open(os.getcwd() + r"\lexicons\assertives_hooper1975.txt").read().split('\n')
        factiveTwoWords = open(os.getcwd() + r"\lexicons\factive_twowords2.txt","r").read().split('\n')
        factiveTwoWords2 = open(os.getcwd() + r"\lexicons\factive_twowords.txt","r").read().split('\n')
        factives = open(os.getcwd() + r"\lexicons\factives_hooper1975.txt","r").read().split('\n')
        hedgeTwoWords = open(os.getcwd() + r"\lexicons\hedges_twowords2.txt","r").read().split('\n')
        hedgeTwoWords2 = open(os.getcwd() + r"\lexicons\hedges_twowords.txt","r").read().split('\n')
        hedges = open(os.getcwd() + r"\lexicons\hedges_hyland2005.txt","r").read().split('\n')
        
        pContainer = []
        pHold = []
        nContainer = []
        nHold = []
        fillerContainer = []
        fillerHold = []
        assertiveContainer = []
        assertiveHold = []
        factiveContainer = []
        factiveHold = []
        hedgeContainer = []
        hedgeHold = []
        
        strMaster = ""
        listMaster = []

        sentimentMaster = self.sentimentAnalysis(self.textScraper(os.getcwd() + r'\textResponses'))

       # for i in range(len(positive)):
        #    pInstances = (self.entityCount(sentimentMaster[0],positive[i]))
         #   pContainer.append(pInstances)
          #  if pInstances != 0:
                #print("The word <{}> was used {} times. (p)".format(positive[i],pInstances))
           #     pHold.append(positive[i])

        for i in range(len(negative)):
            nInstances = (self.entityCount(sentimentMaster[0],negative[i]))
            nContainer.append(nInstances)
            if nInstances !=0:
                #print("The word <{}> was used {} times.(n)".format(negative[i],nInstances))
                nHold.append(negative[i])
        
        for i in range(len(fillerOneWord)):
            fillerInstances = (self.entityCount(sentimentMaster[0], fillerOneWord[i]))
            fillerContainer.append(fillerInstances)
            if fillerInstances != 0:
                #print("The word <{}> was used {} times.(filler)".format(fillerOneWord[i],fillerInstances))
                fillerHold.append(fillerOneWord[i])
                
        for i in range(len(fillTwoWords)):
            fillerInstances = str(sentimentMaster[0]).replace(" ", "").count(fillTwoWords[i])
            fillerContainer.append(fillerInstances)
            if fillerInstances != 0:
                #print("The words <{}> were used {} times.(filler)".format(fillTwoWords2[i], fillerInstances))
                fillerHold.append(fillTwoWords2[i])
                
     #   for i in range(len(assertives)):
      #      assertiveInstances = (self.entityCount(sentimentMaster[0], assertives[i]))
       #     assertiveContainer.append(assertiveInstances)
        #    if assertiveInstances != 0:
         #       print("The word <{}> was used {} times.(assertive)".format(assertives[i],assertiveInstances))
          #      assertiveHold.append(assertives[i])
                
        for i in range(len(factiveTwoWords)):
            factiveInstances = str(sentimentMaster[0]).replace(" ", "").count(factiveTwoWords[i])
            factiveContainer.append(factiveInstances)
            if factiveInstances != 0:
                #print("The words <{}> were used {} times.(factive)".format(factiveTwoWords2[i], factiveInstances))
                factiveHold.append(factiveTwoWords[i])
        
        for i in range(len(factives)):
            factiveInstances = (self.entityCount(sentimentMaster[0], factives[i]))
            factiveContainer.append(factiveInstances)
            if factiveInstances != 0:
                #print("The word <{}> was used {} times.(factive)".format(factives[i],factiveInstances))
                factiveHold.append(factives[i])
        
        for i in range(len(hedgeTwoWords)):
            hedgeInstances = str(sentimentMaster[0]).replace(" ", "").count(hedgeTwoWords[i])
            hedgeContainer.append(hedgeInstances)
            if hedgeInstances != 0:
                #print("The words <{}> were used {} times.(hedge)".format(hedgeTwoWords2[i], hedgeInstances))
                hedgeHold.append(hedgeTwoWords[i])

        for i in range(len(hedges)):
            hedgeInstances = (self.entityCount(sentimentMaster[0], hedges[i]))
            hedgeContainer.append(hedgeInstances)
            if hedgeInstances != 0:
                #print("The word <{}> was used {} times.(hedge)".format(hedges[i],hedgeInstances))
                hedgeHold.append(hedges[i])

        strMaster = ''.join(map(str,sentimentMaster[0]))
        listMaster = list(strMaster.split(" "))
        #print(np.argsort(nContainer))
        #print(np.argsort(sentimentMaster[1]))
        #print(sum(nContainer))
        #print(listMaster)
        #print(len(listMaster))
        
        if len(listMaster) == 0:
            length = 1
        else:
            length = len(listMaster)

        nRatio = sum(nContainer)/length
        #pRatio = sum(pContainer)/len(listMaster)
        fillerRatio = sum(fillerContainer)/length
        #assertRatio = sum(assertiveContainer)/length
        factiveRatio = sum(factiveContainer)/length
        hedgeRatio = sum(hedgeContainer)/length

        print(self.nRatioTransform(nRatio))
        print("Your responses contained {:.0%} filler words.".format(fillerRatio))
        #print("Your responses contained {:.0%} assertive words.".format(assertRatio))
        print("Your responses contained {:.0%} factive words.".format(factiveRatio))
        print("Your responses contained {:.0%} hedge words.".format(hedgeRatio))

        if nRatio >.2:
                print("{}".format(nHold + hedgeHold))
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
            
            print(tempStr)
            print('Your {} response produced the following score'.format(p.ordinal(y)))
            print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

            qualScore = self.scoreTransform(sentiment.score)
            sentScore = sentiment.score
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
