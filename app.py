from fastapi import FastAPI
from fastapi import status, Form
from fastapi.param_functions import Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from db import *

app = FastAPI()
app.mount("/ui", StaticFiles(directory = "ui"), name = "ui")
oath2_scheme = OAuth2PasswordBearer(tokenUrl = "/token")
@app.get("/db")
def get_db():
    return create_tables()

@app.get("/user")
def get_user(token = Depends(oath2_scheme)):
    user = get_user_from_token(token)
    return get_user_from_token(token)


@app.get("/Clear")
def clear_db():
    return clear_table()

@app.post("/message/{room}")
def post_message(room: str, message: Message ,username = Depends(get_user)):

    return post_message_to_room(room, message, username)

@app.post("/login")
def post_login(username: str = Form(...), password: str = Form(...)):
    UserData.user = username
    UserData.password = password
    if  verify_user(UserData):
        response = RedirectResponse("/ui/index.html", status.HTTP_302_FOUND)
        response.set_cookie(key = "token", value = get_user_token(username))
        return response
    else:
        return RedirectResponse("/ui/login.html?error=True", status.HTTP_302_FOUND)

@app.get("/message/{room}")
def get_message(room: str, username = Depends(get_user)):

    print(get_message_from_room(room))    
    return get_message_from_room(room)

