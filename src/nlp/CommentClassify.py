# -*- coding: utf-8 -*-
'''
Created on 2015年11月29日

The coding is a little bit messy, it'll be organized later.
@author: Hk
'''
from xml.dom import minidom

import nltk
from nltk.corpus import stopwords

from nlp.DataExtrator import DataExtrator

class CommentClassify(object):
    global general,yesno,questionMarks,apieceN
    apieceN=3
    general="GENERAL"
    yesno="YES_NO"
    #N/A型的问题没必要相似运算
#     questionMarks=['Good','Bad','Potential','Dialogue','non-English','Other','Yes','No','Unsure','Not Applicable','NoDisplay']
    questionMarks=['Good','Bad','Potential','Dialogue','non-English','Other','Yes','No','Unsure','NoDisplay']
    
    def __init__(self):
        '''
        Constructor
        '''
    def selectTopNWords(self,obj):
        topNWordsCount=apieceN*11
        splitWords=[]
        topNWords=[]
        tokens=[]
        all_words={}
        if isinstance(obj, basestring):
            tokens=nltk.word_tokenize(obj)
        elif isinstance(obj, list) and obj:
            for innerList in obj:
                if innerList:
                    tempList=[]
                    for sentence in innerList:
                        wordTokens=nltk.word_tokenize(sentence)
                        tokens.extend(wordTokens)
                        tempList.append(wordTokens)
                    splitWords.append(tempList)
                else:
                    splitWords.append([])
        stopword = stopwords.words('english')
        filterWordsList = [w for w in tokens if w.lower() not in stopword and self.isDigit(w.lower())==False]
        for word in filterWordsList:  
            if word in all_words.keys():  
                all_words[word] += 1  
            else:  
                all_words[word] = 1  
        filterWords = sorted(all_words.items(), key=lambda e:e[1], reverse=True)
        if len(filterWords)>topNWordsCount:
            for t in range(0, topNWordsCount, 1):  
                topNWords.append(filterWords[t][0]) 
        else:
            for t in range(0, len(filterWords), 1):  
                topNWords.append(filterWords[t][0]) 
            for t in range(len(filterWords)+1,topNWordsCount,1):
                topNWords.append('NOP'+bytes(t)) 
        if len(topNWords)<1:
            for t in range(0, topNWordsCount, 1):
                topNWords.append('NOP'+bytes(t))
        return topNWords,splitWords;
    
    def isDigit(self,s):
        s=s.replace(",","")
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False
    
    #'Good','Bad','Potential','Dialogue','non-English','Other','Yes','No','Unsure'
    #分别在question，good，bad，potential，dialogue取top10个词作为它们的特征值
    def generateFeatures(self,qtype,qBody,commentNodeList):
        allList=[]
        goodComments=[]
        badComments=[]
        potentialComments=[]
        dialogueComments=[]
        nonEnglishComments=[]
        otherComments=[]
        yesComments=[]
        noComments=[]
        unsureComments=[]
        naComments=[]
        noDisplayComments=[]
#         qBodyFeatures=DataExtrator.selectTopNWords(qBody);
        
        for node in commentNodeList:
            cid = DataExtrator.getAttrValue(node, 'CID')
            cuser = DataExtrator.getAttrValue(node, 'CUSERID')
            cgold = DataExtrator.getAttrValue(node, 'CGOLD')
            cgold_yn = DataExtrator.getAttrValue(node, 'CGOLD_YN')
            cBody=DataExtrator.getNodeValue(DataExtrator.getXMLNode(node, 'CBody')[0])
            
            if qtype == general:
                if cgold==questionMarks[0]:
                    goodComments.append(cBody)
                elif cgold==questionMarks[1]:
                    badComments.append(cBody)
                elif cgold==questionMarks[2]:
                    potentialComments.append(cBody)
                elif cgold==questionMarks[3]:
                    dialogueComments.append(cBody)
                elif cgold==questionMarks[4]:
                    nonEnglishComments.append(cBody)
                elif cgold==questionMarks[5]:
                    otherComments.append(cBody)
                #NA问题没必要进行相似运算
#                 elif cgold==questionMarks[9]:
#                     naComments.append(cBody)
                else:
                    noDisplayComments.append(cBody)
            elif qtype == yesno:#yes_no型问题暂未考虑ctype
                if cgold_yn==questionMarks[6]:
                    yesComments.append(cBody)
                elif cgold_yn==questionMarks[7]:
                    noComments.append(cBody)
                elif cgold_yn==questionMarks[8]:
                    unsureComments.append(cBody)
#                 elif cgold_yn==questionMarks[9]:
#                     naComments.append(cBody)
                else:
                    noDisplayComments.append(cBody)
            #暂时不加入
#             noDisplayComments.append(cBody)
        qBodyList=[qBody]
        allList.append(qBodyList)
        
        allList.append(goodComments)
        allList.append(badComments)
        allList.append(potentialComments)
        allList.append(dialogueComments)
        allList.append(nonEnglishComments)
        allList.append(otherComments)
        
        allList.append(yesComments)
        allList.append(noComments)
        allList.append(unsureComments)
        
#         allList.append(naComments)#N/A答案没必要进行相似运算
        allList.append(noDisplayComments)
        
        topNWords,splitWords=self.selectTopNWords(allList)
        splitWords.pop(0)
        allFeatures=self.getFeatures(topNWords,splitWords);
        return allFeatures,topNWords;
    
    #[({},1)]
    def getFeatures(self,topNWords,splitWords):
        allFeaturesList=[]
        for i in range(0,len(splitWords),1):
            featuresTuple=()
            featuresDict={}
            if splitWords[i]:
                for j in range(0,len(splitWords[i]),1): 
                    for word in topNWords:
                        featuresDict['contains(%s)' %word] = (word in splitWords[i][j])
                    featuresTuple=(featuresDict,i);
#                     print featuresDict
                allFeaturesList.append(featuresTuple)
#         print allFeaturesList
        return allFeaturesList
    
    def getSplitData(self,node):
        qid = DataExtrator.getAttrValue(node, 'QID')
        qcategory = DataExtrator.getAttrValue(node, 'QCATEGORY')
        quserid = DataExtrator.getAttrValue(node, 'QUSERID')
        qtype = DataExtrator.getAttrValue(node, 'QTYPE')
        qgold_yn = DataExtrator.getAttrValue(node, 'QGOLD_YN')
#         print qid,qcategory,quserid,qtype,qgold_yn
        qBody=DataExtrator.getNodeValue(DataExtrator.getXMLNode(node, 'QBody')[0])
        commentNodeList=DataExtrator.getXMLNode(node, 'Comment')
        return qid,qcategory,quserid,qtype,qgold_yn,qBody,commentNodeList
    
    def getTestData(self,testQtype,testQBody,testCommentNodeList,trainTopNWords):
        testData=[]
        cidList=[]
        for commentNode in testCommentNodeList:
            cid = DataExtrator.getAttrValue(commentNode, 'CID')
            cuser = DataExtrator.getAttrValue(commentNode, 'CUSERID')
            cgold = DataExtrator.getAttrValue(commentNode, 'CGOLD')
            cgold_yn = DataExtrator.getAttrValue(commentNode, 'CGOLD_YN')
            cBody=DataExtrator.getNodeValue(DataExtrator.getXMLNode(commentNode, 'CBody')[0])
            testTopNWords,splitWords=self.selectTopNWords(testQBody+cBody);
            allFeatures=self.getFeatures(trainTopNWords,[[testTopNWords]]);
            #这里仅为利用已有方法而做的结构变化
            testData.append(allFeatures[0][0])
            cidList.append(cid)
        return testData,cidList
    
    def addDict(self,dict,word,word2,pagenumber):
        if dict.has_key(word):
            dict[word].setdefault(word2, []).append(pagenumber)
        else:
            dict[word]={}
            dict[word].setdefault(word2, []).append(pagenumber)
    
    def getPredictResult(self,resultDict):
        retDict={}
        maxValue=0
        maxIndex=0
        for (k,v) in resultDict.items():
            aggregateDict={}
            for(k2,v2) in v.items():
#                 aggregateDict[k2]=sum(v2)/len(v2)
                aggregateDict[k2]=sum(v2)
            for (k3,v3) in aggregateDict.items():
                if maxValue<v3:
                    maxIndex=k3
                    maxValue=v3
            retDict[k]=maxIndex
        return retDict
    
    def appendFile(self,allLevelDict,filePath):
        output = open(filePath, 'a')
        if filePath.find("task1")!=-1:
            for (k,v) in self.getPredictResult(allLevelDict).items():
                output.write(k+'\t'+v+"\r")
                print k,'\t',v
        else:
            yesnoDict={}
            key=""
            maxLabelCount=0
            maxLabel=""
            for (k,v) in self.getPredictResult(allLevelDict).items():
                key=k.split("_")[0]
                self.addDict(yesnoDict, key, v, 1)
            if yesnoDict.get(key):
                for (k2,v2) in yesnoDict.get(key).items():
                    if maxLabelCount<len(v2):
                        maxLabelCount=len(v2)
                        maxLabel=k2
            else:
                output.write(key+"~~~~~~~~~~~~~~~~~~~~~~~~~noData")
            output.write(key+'\t'+maxLabel+"\r")
            print key,'\t',maxLabel
        output.close()
    
    def getPredictsData(self,traiFileName,testFileName,generalFile,yesnoFile):
        trainRoot = minidom.parse(traiFileName).documentElement
        testRoot = minidom.parse(testFileName).documentElement
    
        testQuestions = DataExtrator.getXMLNode(testRoot, 'Question')
        trainQuestions = DataExtrator.getXMLNode(trainRoot, 'Question')
        for i in range(0,len(testQuestions),1):
            allLevelDict={}
            testQid,testQcategory,testQuserid,testQtype,testQgold_yn,testQBody,testCommentNodeList=self.getSplitData(testQuestions[i])
#             print testDict
            for node in trainQuestions:
                trainQid,trainQcategory,trainQuserid,trainQtype,trainQgold_yn,trainQBody,trainCommentNodeList=self.getSplitData(node)
#                 if testQcategory==trainQcategory and trainQtype==testQtype:
#                 if testQcategory==trainQcategory and trainQtype==testQtype and testQtype=='YES_NO':
                if testQcategory==trainQcategory and trainQtype==testQtype:
                    trainData,topNWords=self.generateFeatures(trainQtype,trainQBody,trainCommentNodeList)
                    testData,cidList=self.getTestData(testQtype,testQBody,testCommentNodeList,topNWords)
    #                 print trainQid,trainData
                    if trainData:
                        classifier = nltk.NaiveBayesClassifier.train(trainData)
    #                     print nltk.classify.accuracy(classifier,testData)
    #                     classifier.classify_many(testData)
    #                     print classifier.classify(testDict)
                        labelList=sorted(classifier.labels())
#                         print labelList
                        pdist=classifier.prob_classify_many(testData)
                        print('[TEST]:%s - %s \r\n[TRAIN]:%s - %s' %(testQid,testQBody,trainQid,trainQBody))
                        for j in range(0,len(pdist),1):
                            for label in labelList:
                                if pdist[j].prob(label)!=0 and pdist[j].prob(label)!=1 and pdist[j].prob(label)!=0.5:#去除prob为0和1的值
                                    self.addDict(allLevelDict,cidList[j],questionMarks[label],pdist[j].prob(label))
                                print('第%s个comment属于%s的概率: %.4f' %(j+1,questionMarks[label],pdist[j].prob(label)))
                    else:
                        print 'It does not have dataset..'
#             break;
#             print 'The 1th round of loop ended'
            if testQtype=='YES_NO':
                self.appendFile(allLevelDict,yesnoFile);
            else:
                self.appendFile(allLevelDict,generalFile);
                
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Question number'+bytes(i+1)+' finished'
            