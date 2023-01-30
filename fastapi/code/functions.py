from jinja2 import Template
import json
import os
import couchdb
from datetime import datetime
import pytz


def now():
    now = datetime.now(pytz.timezone('Europe/Amsterdam'))
    return datetime.strftime(now, '%Y-%m-%d-%H:%M:%S')


def getdb(dbname, **kwargs):
    user = "admin"
    password = "mysecretpassword"
    dbhost =  "couchdb"
    couchserver = couchdb.Server(f"http://{user}:{password}@{dbhost}:5984/")
    if dbname in couchserver:
        db = couchserver[dbname]
        if kwargs.get('delete', False):
            del couchserver[dbname]
            return f"Deleted {dbname} db"
    else:
        db = couchserver.create(dbname)
    return db


def getdocs(type, expanded, **kwargs):
    filter = {k:v for (k,v) in kwargs.items() if v != None}
    if filter.get('query', False):
        try:
            mango = {'selector': eval(kwargs['query'])}
        except:
            return {'msg': 'Query is not a dictionary'}
        return [doc for doc in getdb(f'{type}_objects').find(mango)]
    if bool(filter):
        mango = {'selector': filter}
        return [doc for doc in getdb(f'{type}_objects').find(mango)]
    return [doc.get('doc', doc['id']) for doc in getdb(f"{type}_objects").view('_all_docs', include_docs=expanded)]


def createdoc(type, payload, **kwargs):
    doc = payload.dict()
    doc['date_created'] = now()
    if kwargs.get('key', False):
        k = kwargs['key']
        mango = {'selector': {k: doc[k]}}
        docs = [doc for doc in getdb(f'{type}_objects').find(mango)]
        if len(docs) > 0:
            return False, 422, f"{type.title()} already exists"
    id = getdb(f'{type}_objects').save(doc)[0]
    return True, 201, getdb(f'{type}_objects').get(id)
    

def getdocbyid(type, id, **kwargs):
    doc = getdb(f'{type}_objects').get(id)
    if not bool(doc):
        return False, 404, f"{type.title()} not found"
    return True, 200, doc


def updatedoc(type, id, payload, **kwargs):
    doc = getdb(f'{type}_objects').get(id)
    if not bool(doc):
        return False, 404, f"{type.title()} not found"
    ref = doc.copy()
    doc.update(payload.dict())
    if doc == ref:
        return False, 422, f"{type.title()} no change detected"
    doc['date_updated'] = now()
    id = getdb(f'{type}_objects').save(doc)[0]
    return True, 200, getdb(f'{type}_objects').get(id)