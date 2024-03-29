from fastapi import FastAPI, HTTPException, Header, Response
from pydantic import BaseModel, constr
from sqlalchemy import func, select
from datetime import datetime 
import sys

app = FastAPI()

from pathlib import Path
current_dir = Path(__file__).resolve().parent

from database.core import *
from database.user import * 
from database.application import *

from model import *
from tools import *

Base.metadata.create_all(
    bind=engine
)  

@app.post("/api/register", tags=["register"])
async def register(data: Register_example): 
    if data.password != data.re_pw:
        return {"비밀번호가 일치하지 않습니다."}

    hashed_pw = hashing_pw(
        data.password
    ) 

    db_user = User( 
        username=data.username,
        password=hashed_pw,
        school_id=data.school_id,
    )

    with SessionLocal() as db:  
        db.add(db_user)  
        db.commit()

    return {"ok": "True"}

@app.post("/api/login", tags=["login"])
async def login(data: Login_example):
    pw = data.password
    hashed_pw = hashing_pw(pw)
    
    with SessionLocal() as db:  
        user = db.query(User).filter(User.username == data.username, User.password == hashed_pw).first()

    if not user:
        return {"아이디 혹은 비밀번호가 다릅니다."}

    elif user.role == 'admin':
        token = admin_Token(user.id)
        return ({"ok": "true"}, token) 
    
    token = encToken(user.id)
    return ({"ok": "true"}, token)

@app.post("/api/application", tags=["application"]) # 임시저장 엔드포인트 
async def application(data : Application_example, token : str = Header(...)):
    user = check_auth(token)
    
    if not user: 
        return {"로그인 후 이용 가능합니다."}
    
    db_value = Application(
        bio = data.bio,
        motive = data.motive,
        plan = data.plan,
        which_department = data.which_department,
        user_id = user,
        last_modified=datetime.now().isoformat()
    )
    
    with SessionLocal() as db:  
        db.add(db_value)  
        db.commit()

    return {"ok": "True"}

@app.post("/api/final_submit", tags=["application"]) # 최종제출 엔드포인트
async def final_submit(data : Application_example, token : str = Header(...)):
    user = check_auth(token)
    
    with SessionLocal() as db: 
        user_info = db.query(User).filter(User.id == user).first()
        
    if user_info.is_submitted == True:
        raise {"ok": "False", "message":"이미 제출하셨습니다."}
    
    db_value = Application(
        bio = data.bip,
        motive = data.motive,
        plan = data.plan,
        which_department = data.which_department,
        user_id = user,
        last_modified=datetime.now().isoformat()
    )
    
    with SessionLocal() as db:  
        db.add(db_value)  
        db.commit()
    
    return {"ok": "True"}


@app.get("/api/show_apply", tags=["application"]) # 임시저장 불러오기
async def showApply(token : str = Header(...)):
    user = check_auth(token)
    
    if not user:
        return {"ok":"False", "message":"토큰이 올바르지 않습니다."}
    
    with SessionLocal() as db:
        subquery = (
            db.query(func.max(Application.id).label('max_id'))
            .filter(Application.user_id == user)
            .group_by(Application.which_department)
        ).subquery()

        latest_applications = (
            db.query(Application)
            .join(subquery, Application.id == subquery.c.max_id)
            .all()
        )

    return {"ok":"True", "value":latest_applications}

@app.post("/api/authcheck", tags=["authcheck test"])
async def authcheck(token : str = Header(...)):
    user = check_auth(token)
    
    if not user:
        return {"ok":"False"}
    
    return {"recived_token": token}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
