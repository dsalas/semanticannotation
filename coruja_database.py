from configparser import ConfigParser
import pymysql
import api_log

def read_db_config(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    return db

def connect():
    config = read_db_config()
    db = pymysql.connect(config["host"],config["user"],config["password"],config["database"])
    return db

def getVersion():
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    api_log.log("Database version : %s " % data)
    db.close()
    return data

def insertOntology(uri,name, path):
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO ontologia (Tx_OntUri, \
       No_OntNombreArchivo, Tx_OntUbicacion) \
       VALUES ('%s', '%s', '%s')" % \
          (uri, name, path)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def insertDocument(uri, name):
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO documento (Tx_DocUri, \
       Bo_DocProcesado, Tx_DocNombreArchivo) \
       VALUES ('%s', '%d', '%s')" % \
          (uri, 1, name)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def getActiveOntologies():
    db = connect()
    cursor = db.cursor()
    ontofiles = []
    try:
        cursor.execute("SELECT * FROM ontologia WHERE Bo_OntHab = 1")
        results = cursor.fetchall()
        for row in results:
            file = row[2]
            path = row[3]
            ontofile = path+file
            ontofiles.add(ontofile)
            # Now print fetched result
            api_log.log("Active ontology: " + ontofile)
    except:
        api_log.log("Error: unable to fetch data")
    db.close()
    return ontofiles