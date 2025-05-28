from typing import Union
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates # for rendering html pages
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


app = FastAPI()

app.mount('/static',StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates') # this is pointing to directory from where html is rendered


@app.get("/",response_class=HTMLResponse)
def read_root(request:Request):
    return templates.TemplateResponse(
        request=request ,
        name = 'index.html'
    )

@app.get("/api")
def read_msg():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}