'''
Created on Thu Oct 31 2019 4:35:36 PM
Author: ajithkumar-natarajan
Copyright (c) 2019 -- The MIT License (MIT)
'''

# -*- coding: utf-8 -*-

import json
# if you are using python 3, you should
import urllib.request
from urllib.parse import urlparse
import os.path

models=['BM25', 'DFR', 'LM']
# models=['language_model','BM25','DFR']
queries = open("test_queries.txt", encoding="utf-8")
# queries = open("queries.txt", encoding="utf-8")

for query in queries:
    text = query.partition(' ')[2]
   
    text = text.replace(':','\:')
    text_en = 'text_en:'+urllib.parse.quote(text)
    text_ru = 'text_ru:'+urllib.parse.quote(text)
    text_de = 'text_de:'+urllib.parse.quote(text)
    for IRModel in models:
        # inurl = 'http://18.223.122.91:8983/solr/#/'+IRModel+'/select?q='+text_en+'%20'or'%20'+text_ru+'%20'or'%20'+text_de+'&fl=id%2Cscore&wt=json&indent=true&rows=20'
        inurl = 'http://18.223.122.91:8983/solr/'+IRModel+'/select?q='+text_en+'%20or%20'+text_ru+'%20or%20'+text_de+'&fl=id%2Cscore&wt=json&indent=true&rows=20'
        

        # change query id and IRModel name accordingly
        query_id = query.partition(' ')[0]
        # print(query_id)
        
        if not os.path.exists(IRModel):
            os.makedirs(IRModel)
        
        output_file_name = query_id + IRModel + ".txt"
        consolidated_output_file_name = IRModel + ".txt"
        # output_file = output_file_name
        output_file = os.path.join(IRModel, output_file_name)
        consolidated_output_file = os.path.join(IRModel, consolidated_output_file_name)
        file = open(output_file, 'w')
        consolidated_file = open(consolidated_output_file, 'a+')
        #data = urllib.urlopen(inurl)
        # if you're using python 3, you should use
        # print(inurl)
        data = urllib.request.urlopen(inurl)

        docs = json.load(data)['response']['docs']
        # the ranking should start from 1 and increase
        rank = 1
        for doc in docs:
            file.write(query_id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
            consolidated_file.write(query_id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
            rank += 1
file.close()
print("Process completed")