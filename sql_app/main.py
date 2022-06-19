from typing import List, Union
from uuid import UUID
from fastapi import FastAPI, Response, UploadFile, status, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
# from dependencies import CommonParams, verify_app_headers
from . import models, schema, crud
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


# app = FastAPI(dependencies=[Depends(verify_app_headers)])
app = FastAPI()

origins = [
    "http://localhost.wahab.com",
    "https://localhost.wahab.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user_ = crud.get_user_by_email(db, email=user.email)
    if user_:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schema.Item)
def create_item_for_user(
    user_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# status_code=status.HTTP_200_OK, response_model=User, summary="Get Users"
# dependencies=[Depends(verify_app_headers)]
# @app.get("/")
# async def read_root(response: Response, request: CommonParams = Depends(CommonParams)):
#     """
#     Descriptions written in markdown.
#     """
#     response = {}
#     if request.q:
#         response.update({"q": request.q})
#     items = fake_items_db[request.skip : request.skip + request.limit]
#     response.update({"items": items})
#     return response


# @app.get("/{user_id}")
# async def retrieve_user(user_id: UUID, q: Union[str, None] = None):
#     return { "user_id": user_id, "q": q }


# @app.post("/upload")
# async def upload(file: UploadFile):
#     return { "file": file.filename }


# @app.patch("/{user_id}")
# async def update_user(user_id: UUID, user: User):
#     return { 'item_id': user_id, "name": user.first_name, "gender": user.gender, "roles": user.roles }

