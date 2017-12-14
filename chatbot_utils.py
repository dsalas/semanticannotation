import pandas as pd
import numpy as np
import os
from nltk.tag import StanfordPOSTagger
import pandas as pd
from gensim.models.keyedvectors import KeyedVectors

def describe_stanford_pos_tag(pos_tag):
    df = pd.read_csv("/var/www/pyapi/scripts/Stanford_POS_Tags.csv")
    result = df.loc[df['code'] == pos_tag[1]]
    row = result.iloc[0]
    label = row['description']
    type = row['type']
    return (pos_tag[0],label, type)

def lemmatize(token, lemmaDict):
    lemmaDict.columns = ["lemma", "token"]
    lemma = token
    result = lemmaDict.loc[lemmaDict["token"] == token]
    if len(result) > 0:
        lemma = result.iloc[0]["lemma"]
    return lemma


def calculate_distance(word, word_list, model):
    total_distance = 0.0
    size = len(word_list)
    for item in word_list:
        total_distance += model.similarity(word, item)
    return (total_distance / size)

def getTaggedQuestion(question):
    os.environ["STANFORD_MODELS"] = "/home/jedda/scpDocs/stanford-postagger-full-2017-06-09/models"
    spanish_postagger = StanfordPOSTagger('spanish.tagger', '/home/jedda/scpDocs/stanford-postagger-full-2017-06-09/stanford-postagger.jar')
    tagged_question = []
    tagged = spanish_postagger.tag(question.split())
    for tag in tagged:
        tag_triple = describe_stanford_pos_tag(tag)
        tagged_question.append(tag_triple)
    return tagged_question

def getQuestionWords(tagged_question):
    interjections = []
    verbs = []
    words = []
    lemmaDict = pd.read_csv('/var/www/pyapi/scripts/lemmatization-es.txt', sep="\t", header=None)
    print("lemmaDict created")
    for tag_triple in tagged_question:
        if tag_triple[2] == "Interjections":
            words.append(tag_triple[0])
            interjections.append(tag_triple[0])
        if tag_triple[2] == "Verbs":
            verb = lemmatize(tag_triple[0].lower(), lemmaDict)
            words.append(verb)
            verbs.append(verb)
    return (words, interjections, verbs)

def getCategoriesDistance(question_data, categories):
    #categories = ["restaurante", "cine", "bar", "tienda"]
    categories_distance = []
    print("loading word vector")
    #model = KeyedVectors.load_word2vec_format("/home/jedda/scpDocs/w2vmodel/SBW-vectors-300-min5.txt", binary=False)
    model = KeyedVectors.load("/home/jedda/scpDocs/wordvectors")
    print("word vector ready")
    for category in categories:
        distance = calculate_distance(category, question_data[0],model)
        categories_distance.append((category,distance))
    return categories_distance

def getCategory(question, categories):
    tagged_question = getTaggedQuestion(question.replace('?',''))
    question_data = getQuestionWords(tagged_question)
    categories_distance = getCategoriesDistance(question_data, categories)
    best_category = ""
    best_distance = 0.0
    for item in categories_distance:
        if item[1] > best_distance:
            best_distance = item[1]
            best_category = item[0]
    return best_category
