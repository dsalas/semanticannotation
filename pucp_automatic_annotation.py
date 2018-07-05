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

def _getText(filename):
    text = textract.process(filename, method='pdfminer')
    decoded = text.decode("utf-8")
    return decoded

def _clean(text):
    clean = text.replace("\n", " ").replace("´", "").replace(".", "").replace(",", "").replace(":", "")
    words = clean.split(" ")
    words = list(filter(lambda x: len(x) > 2, words))
    clean_words = []

    stopwords = set(nltk.corpus.stopwords.words('spanish'))

    for word in words:
        if word.isalpha():
            if not word.lower() in stopwords:
                clean_words.append(word)
    result = " ".join(clean_words)
    return result

def _createSet(tagged_results):
    concepts = set([])
    for element in tagged_results:
        if element[2] == "Interjections":
            concepts.add(element[0])
    return concepts

def createBaseOntology(filename, filepath):
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
    return onto_file.name, filenameOwl, uri

def createOntology(document, concepts):
    onto = get_ontology(config.OntologyNamespace + "test_ontology.owl")
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

    documentTest = Document(document)
    for concept in concepts:
        ontoConcept = Concept(concept)
        documentTest.documentHasConcept.append(ontoConcept)
    onto_file = open("/var/www/pyapi/scripts/persist/ontology.owl", 'wb+')
    onto.save(file=onto_file, format="rdfxml")

def anotate(filename, path):
    text = _getText(path)
    cleaned = _clean(text)
    tagged_results = tagging_implementation.tag(cleaned)
    concepts = _createSet(tagged_results)
    result = {'document': filename, 'concepts': list(concepts)}
    return result

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

def annotateDocumentInPath(path, ontopath):
    text = _getText(path)
    cleaned = _clean(text)
    tagged_results = tagging_implementation.tag(cleaned)
    concepts = _createSet(tagged_results)
    docid = saveFileToBd(path)
    status = addDocumentConceptsToOntology(docid, ontopath, concepts)
    return status

def annotateDocumentsInPath(path, ontopath):
    files = [f for f in os.listdir(path) if os.path.isfile(path + "/" + f)]
    files = filter(lambda f: f.endswith(('.pdf', '.PDF')), files)
    status = {}
    for file in files:
        filepath = path + "/" + file
        filestatus = annotateDocumentInPath(filepath, ontopath)
        status[filepath] = filestatus
    return status

def saveFileToBd(path):
    ts = round(time.time())
    return ts


def annotateDocumentInPath(path, ontopath):
    text = _getText(path)
    cleaned = _clean(text)
    tagged_results = tagging_implementation.tag(cleaned)
    concepts = _createSet(tagged_results)
    addConceptsToOntology(ontopath, concepts)

def getDocumentsFromOntology(query_concepts):
    path = "./persist/ontology/test.owl"
    onto = get_ontology("file://" + path)
    onto.load()
    with onto:
        sync_reasoner()
    concepts = onto.search(is_a = onto.Concept)
    scores = []
    for concept in concepts:
        score = -1
        for token in query_concepts:
            if score == -1:
                score = editdistance.eval(concept.name, token)
            else:
                score = min(score, editdistance.eval(concept.name, token))
        scores.append((score, concept))
    lowest_scores = list(filter(lambda x: x[0] < 3, scores))
    result = {"documents":[]}
    for score in lowest_scores:
        concept = score[1]
        documents = concept.conceptInDocument
        for document in documents:
            result["documents"].append((document.name))
    return result

def getDocuments(query):
    cleaned = _clean(query)
    tagged_results = tagging_implementation.tag(cleaned)
    query_concepts = _createSet(tagged_results)
    return getDocumentsFromOntology(query_concepts)
