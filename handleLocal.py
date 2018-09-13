import json
def handleLocal(path, data):
    if path == "/test":
        import test as test
        print(test.service(json.loads(data)))
    if path == "/createOnto":
        import ws_create_ontology as createOntology
        print(createOntology.service(json.loads(data)))
    if path == "/updateConcepts":
        import ws_update_concepts as concepts
        print(concepts.service(json.loads(data)))
    if path == "/annotateDocument":
        import ws_annotate_document as annotate
        print(annotate.service(json.loads(data)))
    if path == "/getDocuments":
        import ws_get_documents as getdocs
        print(getdocs.service(json.loads(data)))
    if path == "/getConcepts":
        import ws_get_concepts as getconcepts
        print(getconcepts.service(json.loads(data)))
    if path == "/editConfiguration":
        import ws_edit_configuration as editconf
        print(editconf.service(json.loads(data)))
    if path == "/generateOntodata":
        import ws_generate_ontodata as generateOnto
        print( generateOnto.service(json.loads(data)))
    print("{\"error\":\"Invalid path: " + path + "\"}")