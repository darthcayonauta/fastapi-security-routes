from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
import uvicorn 


app = FastAPI()

#seguridad
SECRET_KEY = "cayofilo-es-la-cumbia"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 30

#modelo del usuario
class User(BaseModel):
    username:str
    password:str

#modelo del token
class Token(BaseModel):
    access_token: str
    token_type: str

#simulacion DB, tambien pdrías probar usando mongodb o mysql
users_db = {
    "user1":{
        "username":"user1",
        "password":"password1"
    },
    "user2":{
        "username":"user2",
        "password":"password2"
    }
}

#funcion que autentica usuario y generación Token JWT
def authenticate_user(user:User):
    if user.username in users_db and user.password == users_db[user.username]["password"]:
        #datos que se incuirán en el token jwt
        user_data = {
            "sub":user.username,
            "exp":datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        #genera el token
        token = jwt.encode(user_data,SECRET_KEY,algorithm=ALGORITHM)
        return Token(access_token=token,token_type="bearer")
    raise HTTPException(status_code=400,detail="Credendiales Incorrectas")

#funcion de dependencia para verificar el token JWT en las rutas protegidas
def get_current_user(token:str = Depends(authenticate_user)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload["sub"]
        if username in users_db:
            return users_db[username]
    except JWTError:
        raise HTTPException(status_code=401,detail="Token inválido")
    raise HTTPException(status_code=401,detail="Usuario no encontrado")

#AHORA EMPIEZA FAST API
@app.post("/login",response_model=Token)
async def login_for_access_token(user:User):
    token = authenticate_user(user)
    return token

#ruta protegida
@app.get("/protected",response_model=dict)
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message":"Ruta Protegida", "user": current_user["username"]}


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)