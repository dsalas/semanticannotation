# -*- coding: utf-8 -*-
import textract
import nltk
import tagging_implementation
from owlready2 import *
import json

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

def createOntology(document, concepts):
    onto = get_ontology("http://test.org/test_ontology.owl")
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

def anotate (filename, path):
    text = _getText(path)
    cleaned = _clean(text)
    tagged_results = tagging_implementation.tag(cleaned)
    concepts = _createSet(tagged_results)
    result = {'document': filename, 'concepts': list(concepts)}
    return result
