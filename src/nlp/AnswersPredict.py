# -*- coding: utf-8 -*-
'''
Created on 2015年11月29日

@author: Hk
'''
from nlp.CommentClassify import CommentClassify

if __name__ == '__main__':
    commentClassify=CommentClassify();
    dataPath="data"
    devFileName="dev.xml"
    trainFileName="train.xml"
    testFileName="test.xml"
    devAnswersQulityFileName="dev-gold.xml"
    devAnswersYNFileName="dev-gold.xml"
    FILE_SEPARATOR="/"
    generalFile="1501220053-test-task1.txt"
    yesnoFile="1501220053-test-task2.txt"
    user_list = commentClassify.getPredictsData(dataPath+FILE_SEPARATOR+devFileName
                                                ,dataPath+FILE_SEPARATOR+devFileName
                                                ,dataPath+FILE_SEPARATOR+generalFile
                                                ,dataPath+FILE_SEPARATOR+yesnoFile)
#     user_list = commentClassify.getPredictsData(dataPath+FILE_SEPARATOR+trainFileName
#                                                 ,dataPath+FILE_SEPARATOR+testFileName
#                                                 ,dataPath+FILE_SEPARATOR+generalFile
#                                                 ,dataPath+FILE_SEPARATOR+yesnoFile)