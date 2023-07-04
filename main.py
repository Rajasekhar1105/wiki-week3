from typing import Optional
from fastapi import FastAPI, Request, Form, status, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import null
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from pydantic import Field, BaseModel


app = FastAPI()

# articlesList = []


templates = Jinja2Templates(directory = "templates")

app.mount("/static", StaticFiles(directory = "static"), name = "static")

models.Base.metadata.create_all(bind = engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Article(BaseModel):
    title: str = Field(min_length = 1)
    content: str = Field(min_length = 1)


@app.get('/')
def home(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.get('/home')
def home_page(request:Request, db:Session=Depends(get_db)):
    return templates.TemplateResponse("home_page.html",{"request":request, "articlesList": db.query(models.articles).all()})

# @app.get('/')
# def home_page(request:Request, db:Session=Depends(get_db)):
#     # articlesList = db.query(models.articles).all()
#     return templates.TemplateResponse("home_page.html", {"request": request, "articlesList": db.query(models.articles).all()})

@app.get('/create')
def create_page(request:Request):
    return templates.TemplateResponse("create.html",{"request":request})

@app.post('/save_article_form_data/', response_model = Article)
async def save_data_response(request:Request, title: str = Form(...), content: str = Form(...), db:Session = Depends(get_db)):
    article_model = models.articles()
    article_model.title = title
    article_model.content = content
    article_data = db.query(models.articles).filter(models.articles.title == title).first()
    if article_data:
        return templates.TemplateResponse("create.html", {"request":request, "details":"* Title : {title} Already exist"})
    db.add(article_model)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home_page"), status_code=status.HTTP_303_SEE_OTHER)

"""
@app.post('/save_article_form_data/')
async def save_data_response(title:str=Form(...),content:str=Form(...)):
    data=article(title=title,content=content)
    articlesList.append(data)
    print(articlesList)
    return RedirectResponse(url=app.url_path_for("home_page"),status_code=status.HTTP_303_SEE_OTHER)
"""