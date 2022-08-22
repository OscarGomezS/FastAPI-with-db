from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.param_functions import Depends

from .database import crud, models, schemas
from .database.database import SessionLocal, engine
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

models.Base.metadata.create_all(bind=engine)
#dependencies=[Depends(get_query_token)]
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/form", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/formhandle", response_class=HTMLResponse)
async def root(request: Request, email: str = Form(...), name: str = Form(...), city: str = Form(...), db: Session = Depends(get_db)):
    user = {"name": name, "email": email, "city": city}
    db_user = crud.get_user_by_email(db, email=user["email"])
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, user=user)
    return templates.TemplateResponse("form_complete.html", {"request": request})

@app.get("/users/", tags=["users"])
async def read_users(request: Request, db: Session = Depends(get_db)):
    result = crud.get_users(db=db)
    return templates.TemplateResponse("details.html", {"request": request, "result": result})
