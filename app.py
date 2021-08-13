from fastapi import FastAPI
from fastapi import status, Form
from fastapi.param_functions import Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pydantic.errors import FrozenSetError
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from db import *
from forgotPassword import *

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

@app.get("/admin")
def get_admin(token = Depends(oath2_scheme)):
    admin = get_admin_from_token
    return get_admin_from_token

@app.get("/Clear")
def clear_db():
    return clear_table()

@app.post("/message/{room}")
def post_message(room: str, message: Message ,username = Depends(get_user)):

    return post_message_to_room(room, message, username)

@app.post("/login")
def post_login(username: str = Form(...), password: str = Form(...), action: str = Form(...)):
    UserData.user = username
    UserData.password = password
    if (action == "signin"):
        if  verify_user(UserData):
            response = RedirectResponse("/ui/index.html", status.HTTP_302_FOUND)
            response.set_cookie(key = "token", value = get_user_token(username))
            return response
        else:
            return RedirectResponse("/ui/404.html", status.HTTP_302_FOUND)
    
    elif (action == "forgot"):

        newPWD = gen_pwd(username, password)
        send_email(username, """\
        Subject: Hello

        Hello user,
        Your new password will be listed below.
        Thank you for your time!
        """+str(newPWD))
        return RedirectResponse("/ui/login.html", status.HTTP_302_FOUND)

@app.post("/ban")
def ban_user(username: str = Form(...)):

    update_banned_user(username)

@app.post("/admin_login")
def post_admin_login(username: str = Form(...), password: str = Form(...)):
    UserData.user = username
    UserData.password = password

    if  verify_admin(UserData):
        response = RedirectResponse("/ui/admin.html", status.HTTP_302_FOUND)
        response.set_cookie(key = "token", value = get_admin_token(username))
        return response
    else:
        return RedirectResponse("/ui/404.html", status.HTTP_302_FOUND)

def no_admin_token():
    
    response = RedirectResponse("/ui/404.html", status.HTTP_302_FOUND)

@app.get("/message/{room}")
def get_message(room: str, username = Depends(get_user)):

    return get_message_from_room(room)

@app.post("/error")
def auth_error():

    return RedirectResponse("/ui/404.html", status.HTTP_302_FOUND)

