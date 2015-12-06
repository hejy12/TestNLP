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
#     user_list = commentClassify.getPredictsData(dataPath+FILE_SEPARATOR+devFileName,
#                                                 dataPath+FILE_SEPARATOR+devFileName)
    user_list = commentClassify.getPredictsData(dataPath+FILE_SEPARATOR+trainFileName,
                                                dataPath+FILE_SEPARATOR+testFileName)