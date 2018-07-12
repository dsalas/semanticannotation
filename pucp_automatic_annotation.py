# -*- coding: utf-8 -*-
import textract
import nltk
import tagging_implementation
from owlready2 import *
import json
import time
import os
sys.path.append('/var/www/pyapi/scripts')
import config
import editdistance
import pandas as pd
import string
import math
from api_log import log

def _getText(filename):
    text = textract.process(filename)
    decoded = text.decode("utf-8")
    return decoded

def _clean(text):
    table = str.maketrans("","",string.punctuation)
    clean = text.translate(table)
    words = clean.split(" ")
    words = list(filter(lambda x: len(x) > 2, words))
    clean_words = []
    nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk-data'))
    stopwords = set(nltk.corpus.stopwords.words('spanish'))
    for word in words:
        if word.isalpha():
            if not word.lower() in stopwords:
                clean_words.append(word)
    result = " ".join(clean_words)
    return result

def _cleanQuery(text):
    table = str.maketrans("","",string.punctuation)
    clean = text.translate(table)
    words = clean.split(" ")
    words = list(filter(lambda x: len(x) > 2, words))
    clean_words = []
    nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk-data'))
    stopwords = set(nltk.corpus.stopwords.words('spanish'))
    for word in words:
        if word.isalpha():
            if not word.lower() in stopwords:
                clean_words.append(word)
    result = " ".join(clean_words)
    return result

def _createList(tagged_results):
    concepts = []
    for element in tagged_results:
        if element[2] == "Interjections":
            concepts.append(element[0])
    return concepts

def _createSet(clean):
    concepts = set([])
    for element in clean.split(" "):
        concepts.add(element)
    return concepts

def createBaseOntology(filename, filepath):
    import coruja_database
    onto = get_ontology(config.OntologyNamespace + filename + ".owl")
    class Document(Thing):
        namespace = onto

    class Concept(Thing):
        namespace = onto

    class documentHasConcept(ObjectProperty):
        namespace = onto
        domain = [Document]
        range = [Concept]

    class conceptInDocument(ObjectProperty):
        namespace = onto
        domain = [Concept]
        range = [Document]
        inverse_property = documentHasConcept

#    class hasId(DataProperty,FunctionalProperty):
#        namespace = onto
#        domain = [Document]
#        range = [int]
    filenameOwl = filename + ".owl"
    uri = config.OntologyNamespace
    onto_file = open(filepath + filenameOwl, 'wb+')
    onto.save(file=onto_file, format="rdfxml")
    coruja_database.insertOntology(uri, filenameOwl, filepath)
    return onto_file.name, filenameOwl, uri

def addConceptsToOntology(path, concepts):
    onto = get_ontology("file://" + path)
    onto.load()
    class Concept(Thing):
        namespace = onto
    for concept in concepts:
        Concept(concept)
    onto_file = open(path, 'wb+')
    try:
        onto.save(file=onto_file, format="rdfxml")
        return True
    except:
        return False

def addDocumentConceptsToOntology(docid, path, concepts):
    onto = get_ontology("file://" + path)
    onto.load()
    class Concept(Thing):
        namespace = onto
    class Document(Thing):
        namespace = onto
    currentDocument = Document(docid)
    class documentHasConcept(ObjectProperty):
        namespace = onto
        domain = [Document]
        range = [Concept]
    for concept in concepts:
        currentConcept = Concept(concept)
        currentDocument.documentHasConcept.append(currentConcept)
    onto_file = open(path, 'wb+')
    try:
        onto.save(file=onto_file, format="rdfxml")
        return True
    except:
        return False

def annotateDocumentInPath(docid, filepath, ontopath):
    log("Call to annotateDocumentInPath()")
    from nltk.tag import StanfordPOSTagger
    os.environ["STANFORD_MODELS"] = os.path.join(os.path.dirname(__file__),'scpDocs/stanford-postagger-full-2017-06-09/models')
    lemmaDict = pd.read_pickle(os.path.join(os.path.dirname(__file__), 'lemmatization-es.pkl'))
    lemmaDict.columns = ["lemma", "token"]
    maxWordDistance = 2
    spanish_postagger = StanfordPOSTagger('spanish.tagger', os.path.join(os.path.dirname(__file__),'scpDocs/stanford-postagger-full-2017-06-09/stanford-postagger.jar'))
    posTagDescDf = pd.read_csv(os.path.join(os.path.dirname(__file__), "Stanford_POS_Tags.csv"))
    ontoDict = {}
    processDocument(docid, filepath, ontoDict, maxWordDistance, posTagDescDf, spanish_postagger, lemmaDict)
    return 1

def processDocument(docid, filepath, ontoDict, maxWordDistance, df, spanish_postagger, lemmaDict):
    text = _getText(filepath)
    cleaned = _clean(text)
    tagged = tagging_implementation.tag(cleaned, df, spanish_postagger)
    concepts = _createList(tagged)
    i=0
    for concept in concepts:
        startIndex = i-maxWordDistance
        if startIndex < 0:
            startIndex = 0
        myNeighbors = concepts[startIndex:maxWordDistance+1+i]
        myNeighbors.remove(concept)
        #myNeighbors contains the range [-3,+3] of words in concepts for current concept
        if concept in ontoDict:
            ontoDict[concept]["count"] = ontoDict[concept]["count"] + 1
            for neighbor in myNeighbors:
                if neighbor in ontoDict[concept]["neighbors"]:
                    ontoDict[concept]["neighbors"][neighbor] = ontoDict[concept]["neighbors"][neighbor] + 1
                else:
                    ontoDict[concept]["neighbors"][neighbor] = 1
        else:
            nearDict = {}
            for neighbor in myNeighbors:
                if neighbor in nearDict:
                    nearDict[neighbor] = nearDict[neighbor] + 1
                else:
                    nearDict[neighbor] = 1
            wordDict = {}
            wordDict["count"] = 1
            ontoDict[concept] = wordDict
            ontoDict[concept]["neighbors"] = nearDict
        ontoDict[concept]["docid"] = docid
        i=i+1

def processOntodict(ontodict, ontopath):
    log("Call to processOntodict()")
    onto = get_ontology("file://" + ontopath)
    onto.load()

    class Concept(Thing):
        namespace = onto

    class Document(Thing):
        namespace = onto

    clases = ontodict['clases']
    concepts = ontodict['concepts']
    for classkey, classelem in clases.items():
        ontoclass = classkey.title()
        with onto:
            NewClass = types.new_class(ontoclass, (Concept,), kwds={})
            for elem in classelem:
                NewClass(elem.lower())

    class documentHasConcept(ObjectProperty):
        namespace = onto
        domain = [Document]
        range = [Concept]

    class conceptInDocument(ObjectProperty):
        namespace = onto
        domain = [Concept]
        range = [Document]

    for concept in concepts:
        docid = concept[1]
        conceptname = concept[0]
        with onto:
            currentDocument = Document(docid)
            currentConcept = Concept(conceptname)
            currentDocument.documentHasConcept.append(currentConcept)
            currentConcept.conceptInDocument.append(currentDocument)

    onto_file = open(ontopath, 'wb+')
    try:
        onto.save(file=onto_file, format="rdfxml")
        log("Saved file to path " + ontopath)
        onto_file.close()
        return True
    except:
        return False

def annotateDocumentsInPath(path, ontopath):
    log("Call to annotateDocumentsInPath()")
    from nltk.tag import StanfordPOSTagger
    import coruja_database
    os.environ["STANFORD_MODELS"] = os.path.join(os.path.dirname(__file__), 'scpDocs/stanford-postagger-full-2017-06-09/models')
    lemmaDict = pd.read_pickle(os.path.join(os.path.dirname(__file__),'lemmatization-es.pkl'))
    lemmaDict.columns = ["lemma", "token"]
    maxWordDistance = 2
    spanish_postagger = StanfordPOSTagger('spanish.tagger',os.path.join(os.path.dirname(__file__), 'scpDocs/stanford-postagger-full-2017-06-09/stanford-postagger.jar'))
    posTagDescDf = pd.read_csv(os.path.join(os.path.dirname(__file__), "Stanford_POS_Tags.csv"))
    files = [f for f in os.listdir(path) if os.path.isfile(path + "/" + f)]
    files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
    status = {}
    ontoDict = {}
    for file in files:
        filepath = path + "/" + file
        log("Procesing " + filepath)
        docid = coruja_database.insertDocument(path + "/",file)
        processDocument(docid, filepath, ontoDict, maxWordDistance, posTagDescDf, spanish_postagger, lemmaDict)
        status[filepath] = 1
    allCount = len(ontoDict)
    tenPCount = math.trunc(0.1 * allCount)
    countList = []
    ontoDictFinal = {"clases": {}, "concepts": set([])}
    for key, element in ontoDict.items():
        countList.append((element["count"], key))
        ontoDictFinal["concepts"].add((key, element["docid"]))

    mainConcepts = sorted(countList, reverse=True)[:tenPCount]

    for mainConcept in mainConcepts:
        validNeighbor = []
        neighborCount = len(ontoDict[mainConcept[1]]["neighbors"])
        neighborTenPCount = math.trunc(0.5 * neighborCount)
        closeNeighbors = sorted(ontoDict[mainConcept[1]]["neighbors"])[:neighborTenPCount]
        for neighbor in closeNeighbors:
            if neighbor != mainConcept[1]:
                if ontoDict[mainConcept[1]]["neighbors"][neighbor] > 1:
                    validNeighbor.append(neighbor)
        if len(validNeighbor) > 0:
            ontoDictFinal["clases"][mainConcept[1]] = set(validNeighbor)
    processOntodict(ontoDictFinal, ontopath)
    return status

def saveFileToBd(path):
    ts = round(time.time())
    return ts

def annotateDocumentInPath(path, ontopath):
    text = _getText(path)
    cleaned = _clean(text)
    tagged_results = tagging_implementation.tag(cleaned)
    concepts = _createList(tagged_results)
    addConceptsToOntology(ontopath, concepts)

def get_concepts(onto):
    #with onto:
    #    sync_reasoner()
    return onto.search(is_a = onto.Concept)

def getDocumentsFromOntology(concepts, ontopath, resultDocuments):
    log("Call to getDocumentsFromOntology(): " + ontopath)
    onto = get_ontology("file://" + ontopath)
    onto.load()
    ontoconcepts = get_concepts(onto)
    scores = []
    for concept in ontoconcepts:
        score = -1
        for token in concepts:
            if score == -1:
                score = editdistance.eval(concept.name, token)
            else:
                score = min(score, editdistance.eval(concept.name,token))
        scores.append((score, concept))
    lowest_scores = list(filter(lambda x: x[0] < 3,scores))
    validConcepts = []
    for score in lowest_scores:
        validConcepts.append(score[1])
    #Expand concepts
    for concept in validConcepts:
        documents = concept.conceptInDocument
        for document in documents:
            if document.name not in resultDocuments:
                resultDocuments.append(document.name)

def processQuery(query,ontoPaths):
    cleaned = _cleanQuery(query)
    concepts = _createSet(cleaned)
    documents = []
    for ontopath in ontoPaths:
        getDocumentsFromOntology(concepts, ontopath, documents)
    return documents

def getDocuments(query):
    import coruja_database
    ontoPaths = coruja_database.getActiveOntologies()
    return processQuery(query, ontoPaths)


def getConcepts(documentId, ontopath):
    onto = get_ontology("file://" + ontopath)
    onto.load()
    document = onto.search(iri =onto.base_iri+str(documentId))[0]
    concepts = document.documentHasConcept
    result = []
    for concept in concepts:
        result.append(concept.name)
    return result


def getConceptsFromOntology(documentId, ontoId):
    import coruja_database
    ontopath = coruja_database.getOntology(ontoId)
    return getConcepts(documentId, ontopath)

def annotateDocumentsInList(docList, ontoId):
    log("Call to annotateDocumentsInPath()")
    import coruja_database
    ontopath = coruja_database.getOntology(ontoId)
    from nltk.tag import StanfordPOSTagger
    import coruja_database
    os.environ["STANFORD_MODELS"] = os.path.join(os.path.dirname(__file__), 'scpDocs/stanford-postagger-full-2017-06-09/models')
    lemmaDict = pd.read_pickle(os.path.join(os.path.dirname(__file__),'lemmatization-es.pkl'))
    lemmaDict.columns = ["lemma", "token"]
    maxWordDistance = 2
    spanish_postagger = StanfordPOSTagger('spanish.tagger',os.path.join(os.path.dirname(__file__), 'scpDocs/stanford-postagger-full-2017-06-09/stanford-postagger.jar'))
    posTagDescDf = pd.read_csv(os.path.join(os.path.dirname(__file__), "Stanford_POS_Tags.csv"))
    status = {}
    ontoDict = {}
    for doc in docList:
        filepath = doc['path']
        docid = doc['id']
        log("Procesing " + filepath)
        processDocument(docid, filepath, ontoDict, maxWordDistance, posTagDescDf, spanish_postagger, lemmaDict)
        status[filepath] = 1
    allCount = len(ontoDict)
    tenPCount = math.trunc(0.1 * allCount)
    countList = []
    ontoDictFinal = {"clases": {}, "concepts": set([])}
    for key, element in ontoDict.items():
        countList.append((element["count"], key))
        ontoDictFinal["concepts"].add((key, element["docid"]))

    mainConcepts = sorted(countList, reverse=True)[:tenPCount]

    for mainConcept in mainConcepts:
        validNeighbor = []
        neighborCount = len(ontoDict[mainConcept[1]]["neighbors"])
        neighborTenPCount = math.trunc(0.5 * neighborCount)
        closeNeighbors = sorted(ontoDict[mainConcept[1]]["neighbors"])[:neighborTenPCount]
        for neighbor in closeNeighbors:
            if neighbor != mainConcept[1]:
                if ontoDict[mainConcept[1]]["neighbors"][neighbor] > 1:
                    validNeighbor.append(neighbor)
        if len(validNeighbor) > 0:
            ontoDictFinal["clases"][mainConcept[1]] = set(validNeighbor)
    processOntodict(ontoDictFinal, ontopath)
    return status

def updateConcepts(docId,ontoId,concepts):
    import coruja_database
    ontopath = coruja_database.getOntology(ontoId)
    onto = get_ontology("file://" + ontopath)
    onto.load()
    result = onto.search(iri=onto.base_iri + docId)
    document = result[0]
    document.documentHasConcept = []
    for concept in concepts:
        ontoconcept = onto.Concept(concept)
        ontoconcept.conceptInDocument.append(document)
    onto_file = open(ontopath, 'wb+')
    onto.save(file=onto_file, format="rdfxml")
    return 1

#createBaseOntology("coruja_edpm", os.path.join(os.path.dirname(__file__),"persist/ontology/"))
#createBaseOntology("coruja_tree", os.path.join(os.path.dirname(__file__),"persist/ontology/"))

#ontoId = 7
#import coruja_database
#ontopath = coruja_database.getOntology(ontoId)
#annotateDocumentsInPath("persist/debug/test_docs/pc_test", ontopath)

#print(getDocuments("punto"))

#print(getConceptsFromOntology(8,7))
