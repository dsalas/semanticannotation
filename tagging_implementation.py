# -*- coding: utf-8 -*-
from nltk.tag import StanfordPOSTagger
import os
import pandas as pd

def _describe_stanford_pos_tag(tagged):
    df = pd.read_csv("/var/www/pyapi/scripts/Stanford_POS_Tags.csv")
    result = []
    for tag in tagged:
        described = df.loc[df['code'] == tag[1]]
        row = described.iloc[0]
        label = row['description']
        type = row['type']
        result.append((tag[0],label, type))
    return result

def _tagging(data):
    os.environ["STANFORD_MODELS"] = "/home/jedda/scpDocs/stanford-postagger-full-2017-06-09/models"
    spanish_postagger = StanfordPOSTagger('spanish.tagger', '/home/jedda/scpDocs/stanford-postagger-full-2017-06-09/stanford-postagger.jar')
    tagged = spanish_postagger.tag(data.split())
    return _describe_stanford_pos_tag(tagged)

def tag(data):
    result = _tagging(data)
    return result