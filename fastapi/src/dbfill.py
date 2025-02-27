import couchdb
from datetime import datetime
import pytz


def now():
    now = datetime.now(pytz.timezone('Europe/Amsterdam'))
    # return datetime.strftime(now, '%Y-%m-%d-%H:%M:%S')
    return now.isoformat()

def getdb(dbname, **kwargs):
    user = "admin"
    password = "secret123"
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


def cleardb():
    getdb('author_objects', delete=True)
    getdb('book_objects', delete=True)


def dbfill():
    authors = ["Harper Lee", "Jane Austen", "George Orwell", "J.D. Salinger", \
               "F. Scott Fitzgerald", "Emily Brontë", "Charlotte Brontë", \
               "Ray Bradbury", "William Golding"]

    books = [{"title": "To Kill a Mockingbird", "author": "Harper Lee"}, \
             {"title": "Pride and Prejudice", "author": "Jane Austen"}, \
             {"title": "1984", "author": "George Orwell"}, \
             {"title": "The Catcher in the Rye", "author": "J.D. Salinger"}, \
             {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}, \
             {"title": "Wuthering Heights", "author": "Emily Brontë"}, \
             {"title": "Jane Eyre", "author": "Charlotte Brontë"}, \
             {"title": "Fahrenheit 451", "author": "Ray Bradbury"}, \
             {"title": "Lord of the Flies", "author": "William Golding"}, \
             {"title": "Persuasion", "author": "Jane Austen"}]


    for a in authors:
        mango = {'selector': {'name': a}}
        if list(getdb('author_objects').find(mango)) == []:
            getdb('author_objects').save({'name': a, 'date_created': now()})

    for b in books:
        mango = {'selector': {'title': b['title']}}
        if list(getdb('book_objects').find(mango)) == []:
            b['date_created'] = now()
            getdb('book_objects').save(b)

    author_docs = getdb('author_objects')
    book_docs = getdb('book_objects')
    print(f"CouchDB has {len(book_docs)} books, by {len(author_docs)} authors")


if __name__ == "__main__":
    dbfill()
