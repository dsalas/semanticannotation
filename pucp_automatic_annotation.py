# -*- coding: utf-8 -*-
#Author Diego Salas
#Date 11/12/2017
import textract
import nltk
import tagging_implementation
import os
import sys
sys.path.append(os.path.dirname(__file__))
import config
import editdistance
import pandas as pd
import string
import math
from api_log import log
#from owlready2 import *
from shutil import copyfile
import gc

def _getText(filename):
    decoded = ""
    try:
        text = textract.process(filename)
        decoded = text.decode("utf-8")
    except:
        log("Could not read document content: " + filename)
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
    text = text.replace('\n', '')
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
    ontofileName = config.OntologyNamespace + filename + ".owl"
    import owlready2
    onto = owlready2.get_ontology(ontofileName)
    log("Creating ontology " + ontofileName)
    class Document(owlready2.Thing):
        namespace = onto

    class Concept(owlready2.Thing):
        namespace = onto

    class documentHasConcept(owlready2.ObjectProperty):
        namespace = onto
        domain = [Document]
        range = [Concept]

    class conceptInDocument(owlready2.ObjectProperty):
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
    try:
        log("Trying to destroy: " + onto.base_iri)
        onto.destroy()
        del onto
    except:
        log("Can't destroy ontology")
    return onto_file.name, filenameOwl, uri

def addDocumentConceptsToOntology(docid, path, concepts):
    import owlready2
    onto = owlready2.get_ontology("file://" + path)
    onto.load()
    class Concept(owlready2.Thing):
        namespace = onto
    class Document(owlready2.Thing):
        namespace = onto

    currentDocument = Document(docid)
    class documentHasConcept(owlready2.ObjectProperty):
        namespace = onto
        domain = [Document]
        range = [Concept]
    for concept in concepts:
        currentConcept = Concept(concept)
        currentDocument.documentHasConcept.append(currentConcept)
    onto_file = open(path, 'wb+')
    try:
        onto.save(file=onto_file, format="rdfxml")
        onto.destroy()
        del onto
        return True
    except:
        onto.destroy()
        del onto
        return False

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

def processOntodict(ontodict, ontopath, mtype):
    log("Call to processOntodict() with ontopath: " + ontopath)
    import owlready2
    onto = owlready2.get_ontology("file://" + ontopath)
    onto.load()

    #class Concept(Thing):
    #    namespace = onto

    #class Document(Thing):
    #    namespace = onto

    clases = ontodict['clases']
    concepts = ontodict['concepts']
    if mtype == 1:
        log("Generating clases...")
        for classkey, classelem in clases.items():
            ontoclass = classkey.title()
            with onto:
                NewClass = owlready2.types.new_class(ontoclass, (onto.Concept,), kwds={})
                for elem in classelem:
                    NewClass(elem.lower())

    for concept in concepts:
        docid = concept[1]
        conceptname = concept[0]
        with onto:
            currentDocumentSearch = onto.search(iri =onto.base_iri+str(docid))
            if len(currentDocumentSearch) > 0:
                currentDocument =  currentDocumentSearch[0]
            else:
                currentDocument = onto.Document(docid)
            currentConceptSearch = onto.search(iri = onto.base_iri + conceptname.lower())
            if len(currentConceptSearch):
                currentConcept = currentConceptSearch[0]
            else:
                currentConcept = onto.Concept(conceptname.lower())
            currentDocument.documentHasConcept.append(currentConcept)
            currentConcept.conceptInDocument.append(currentDocument)

    onto_file = open(ontopath, 'wb+')
    try:
        onto.save(file=onto_file, format="rdfxml")
        log("Saved file to path " + ontopath)
        onto_file.close()
        log("Call to destroy ontolgy: " + ontopath)
        onto.destroy()
        del onto
        del owlready2
        return True
    except:
        log("Error saving ontology, destroying object: " + ontopath)
        onto.destroy()
        del onto
        del owlready2
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
    processOntodict(ontoDictFinal, ontopath, 1)
    return status

def getDocumentsFromOntology(concepts, ontopath, resultDocuments):
    log("Call to getDocumentsFromOntology(): " + ontopath)
    import owlready2
    onto = owlready2.get_ontology("file://" + ontopath)
    try:
        onto.load()
        #with onto:
        #    sync_reasoner()
        log("getDocumentsFromOntology(): Loaded ontology " + ontopath)
    except:
        log("getDocumentsFromOntology(): Error loading ontology " + ontopath)
        return
    log("getDocumentsFromOntology(): Onto world debug: " + str(onto.world.ontologies))
    ontoconcepts = onto.search(is_a = onto.Concept)
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
    try:
        log("getDocumentsFromOntology(): Call to destroy() ontology " + ontopath)
        onto.destroy()
        del onto
        del owlready2
    except:
        log("getDocumentsFromOntology(): Can't destroy ontology " + ontopath)
    gc.collect()

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

def getConcepts(documentId, ontoId):
    import coruja_database
    import time
    log("Call to getConcepts(): docid = " + str(documentId) + " - ontid = " + str(ontoId))
    result = []
    ontopath = coruja_database.getOntology(str(ontoId))
    #Read temp file
    tmpFilename = config.OntologyDir + str(int(time.time())) + "_tmp.owl"
    copyfile(ontopath, tmpFilename)
    log("getConcepts(): Copied ontology from " + ontopath + " to " + tmpFilename)
    import owlready2
    getConceptsOnto = owlready2.get_ontology("file://" + tmpFilename)
    log("getConcepts(): Onto world debug before load: " + str(getConceptsOnto.world.ontologies))
    #getConceptsOnto = get_ontology("file://" + ontopath)
    try:
        getConceptsOnto.load()
        log("getConcepts(): Load ontology :" + tmpFilename)
        #log("getConcepts(): Load ontology :" + ontopath)
    except:
        log("getConcepts(): Error loading ontology " + tmpFilename)
        #log("getConcepts(): Error loading ontology " + ontopath)
        return result
    documents = getConceptsOnto.search(iri =getConceptsOnto.base_iri+str(documentId))
    log("getConcepts(): Onto world debug: " + str(getConceptsOnto.world.ontologies))
    if len(documents) > 0:
        document = documents[0]
        log("getConcepts(): Document found " + document.iri)
        concepts = document.documentHasConcept
        for concept in concepts:
            if concept not in result:
                result.append(concept.name)
        if len(concepts) > 0:
            log("getConcepts(): Concepts found: " + str(len(concepts)))
        else:
            log("getConcepts(): No concepts found.")
    else:
        log("No document found. docid = " + str(documentId))

    os.remove(tmpFilename)
    log("getConcepts(): Deleting temp file " + tmpFilename)
    log("getConcepts(): Trying to destroy " + getConceptsOnto.base_iri )
    try:
        getConceptsOnto.destroy()
        del getConceptsOnto
        del owlready2
        log("getConcepts(): Ontology destroyed")
    except:
        log("getConcepts(): Can not destroy ontology loaded")
    gc.collect()
    return result

def getConceptsFromOntology(documentId, ontoId):
    import coruja_database
    ontopath = coruja_database.getOntology(ontoId)
    if (ontopath == ""):
        return []
    return getConcepts(documentId, ontopath)

def annotateDocumentsInList(docList, ontoId,mtype):
    log("Call to annotateDocumentsInPath() type = " + str(mtype))
    import coruja_database
    ontopath = coruja_database.getOntology(ontoId)
    status = []
    if ontopath == "":
        for doc in docList:
            curr_status = {}
            curr_status["id"] = doc['id']
            curr_status["status"] = 0;
            status.append(curr_status)
        return status
    from nltk.tag import StanfordPOSTagger
    os.environ["STANFORD_MODELS"] = os.path.join(os.path.dirname(__file__), 'scpDocs/stanford-postagger-full-2017-06-09/models')
    lemmaDict = pd.read_pickle(os.path.join(os.path.dirname(__file__),'lemmatization-es.pkl'))
    lemmaDict.columns = ["lemma", "token"]
    maxWordDistance = 2
    spanish_postagger = StanfordPOSTagger('spanish.tagger',os.path.join(os.path.dirname(__file__), 'scpDocs/stanford-postagger-full-2017-06-09/stanford-postagger.jar'))
    posTagDescDf = pd.read_csv(os.path.join(os.path.dirname(__file__), "Stanford_POS_Tags.csv"))
    ontoDict = {}
    for doc in docList:
        filepath = doc['path']
        docid = doc['id']
        log("Procesing " + filepath)
        processDocument(docid, filepath, ontoDict, maxWordDistance, posTagDescDf, spanish_postagger, lemmaDict)
        curr_status = {}
        curr_status["id"] = doc['id']
        curr_status["status"] = 1;
        status.append(curr_status)
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
    processOntodict(ontoDictFinal, ontopath,mtype)
    log("Returning annotation status - finished annotation process")
    return status

def updateConcepts(docId,ontoId,concepts):
    log("Call to updateConcepts()")
    import coruja_database
    ontopath = coruja_database.getOntology(str(ontoId))
    import owlready2
    onto = owlready2.get_ontology("file://" + ontopath)
    log("updateConcepts(): Onto world debug after load: " + str(onto.world.ontologies))
    try:
        onto.load()
        log("updateConcepts(): Load ontology " + ontopath)
    except:
        log("updateConcepts(): Error loading ontology " + ontopath)
        return 0
    log("updateConcepts(): Onto world debug: " + str(onto.world.ontologies))
    log("updateConcepts(): Searching for " + onto.base_iri + str(docId))
    status = 1
    result = onto.search(iri=onto.base_iri + str(docId))
    if (len(result)>0):
        document = result[0]
        ontoConcepts = document.documentHasConcept
        keepConcepts = []
        if len(ontoConcepts) > 0:
            for concept in ontoConcepts:
                if concept.name in concepts:
                    keepConcepts.append(concept)
                else:
                    log("updateConcepts(): Deleting concept: " + concept.name)
            document.documentHasConcept = keepConcepts
        else:
            log("updateConcepts(): No concepts found")
            status = 0
    else:
        status = 0
        log("updateConcepts(): Document not found id="+str(docId))

    if status == 1:
        try:
            # onto_file = open(ontopath, 'wb+')
            onto.save(file=ontopath, format="rdfxml")
            #onto_file.close()
            log("updateConcepts(): Saved ontology to " + ontopath)
        except:
            log("updateConcepts(): Error saving ontology " + ontopath)
            status = 0
    else:
        log("updateConcepts(): Empty ontology loaded " + ontopath)
    try:
        log("updateConcepts(): Destroying ontology " + onto.base_iri)
        #del onto_file
        onto.destroy()
        del onto
        del owlready2
    except:
        log("updateConcepts(): Error destroying ontology:" + onto.base_iri)
    gc.collect()
    return status

