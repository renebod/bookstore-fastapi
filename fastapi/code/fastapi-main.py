from fastapi import FastAPI, Request, Body, Query, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict
from functions import getdocs, createdoc, getdocbyid, updatedoc, updatedocs
from dbfill import dbfill


app = FastAPI()


'''
ONLY FOR DEMO
'''
dbfill()


class Author(BaseModel):
    name: str


@app.get("/")
async def read_root():
    return RedirectResponse("/books", status_code=303)


@app.get("/authors", status_code=200)
async def get_authors(expanded: bool = False,
                      name: str = None,
                      example: int = None,
                      q: str | None = Query(default=None)):
    print(f"Query: {q}")
    return getdocs('author', expanded, name=name, example=example, query=q)
        

@app.post("/authors", status_code=201)
async def create_author(payload: Author):
    success, status_code, result = createdoc('author', payload, key='name')
    if success:
        return result
    else:
        raise HTTPException(status_code=status_code, detail=result) 


@app.get("/authors/{id}", status_code=200)
async def get_author_by_id(id: str):
    success, status_code, result = getdocbyid('author', id)
    if success:
        return result
    else:
        raise HTTPException(status_code=status_code, detail=result) 


@app.put("/authors/{id}", status_code=200)
async def update_author(id: str, payload: Author):
    current = getdocbyid('author', id)[2]
    success, status_code, result = updatedoc('author', id, payload)
    if success:
        updatedocs('book', {'author': current['name']}, {'author': payload.name})
        return result
    else:
        raise HTTPException(status_code=status_code, detail=result)


@app.get("/books", status_code=200)
async def get_books(expanded: bool = False,
                    title: str = None,
                    author: str = None,
                    q: str | None = Query(default=None)):
    return getdocs('book', expanded, title=title, author=author, query=q)