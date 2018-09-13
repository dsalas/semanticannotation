import sys
import json
def handleLocal(path, data):
    if path == "/test":
        import test as test
        print(test.service(json.loads(data)))
        return
    if path == "/createOnto":
        import ws_create_ontology as createOntology
        print(createOntology.service(json.loads(data)))
        return
    if path == "/updateConcepts":
        import ws_update_concepts as concepts
        print(concepts.service(json.loads(data)))
        return
    if path == "/annotateDocument":
        import ws_annotate_document as annotate
        print(annotate.service(json.loads(data)))
        return
    if path == "/getDocuments":
        import ws_get_documents as getdocs
        print(getdocs.service(json.loads(data)))
        return
    if path == "/getConcepts":
        import ws_get_concepts as getconcepts
        print(getconcepts.service(json.loads(data)))
        return
    if path == "/editConfiguration":
        import ws_edit_configuration as editconf
        print(editconf.service(json.loads(data)))
        return
    if path == "/generateOntodata":
        import ws_generate_ontodata as generateOnto
        print( generateOnto.service(json.loads(data)))
        return
    print("{\"error\":\"Invalid path: " + path + "\"}")
    return

path = sys.argv[1]
data = sys.argv[2]
handleLocal(str(path),str(data))
