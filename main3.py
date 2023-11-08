from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn
from datetime import datetime,timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dbClass import *
import os

mongo_host = os.environ.get("HOST_NAME","127.0.0.1")
objDb = Db(mongo_host)

SECRET_KEY = "c583e6ebe05d77b74b5b65277efceffee5ecf806045fcb37f54b29862465f215"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
    "tim":{
            "username":"tim",
            "full_name":"claudio guzman herrera",
            "email":"cguzmanherr@gmail.com",
            "hashed_password":"$2b$12$XF7sCI4pYgR9UyZlvHmWqOiJJ5HOfKbfLTDpPBwzH.icdgyaEOo9O",
            "disabled":False
        }
    }

class Token(BaseModel):
    access_token : str
    token : str

class TokenData(BaseModel):
    username : str or None = None

class User(BaseModel):
    username : str
    email : str or None = None
    full_name : str or None = None
    disabled : bool or None = None

class UserInDb(User):
    hashed_password : str


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db,username:str):
    if username in db:
        user_data = db[username]
        return UserInDb(**user_data)
    
def authenticate_user(db,username:str,password:str):
    user = get_user(db,username)
    if not user :
        return False
    
    if not verify_password(password,user.hashed_password):
        return False

    return user

def create_access_token(data:dict,expires_delta:timedelta or None = None) :
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
         expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="No se pueden validar las credenciales",
                                         headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None :
            raise credential_exception
        
        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exception

    user = get_user(db,username=token_data.username)

    if user is None :
        raise credential_exception
    
    return user


async def get_current_active_user(current_user:UserInDb = Depends(get_current_user)):
    if current_user.disabled :
        raise HTTPException(status_code=400,detail="Usuario inactivo")
    return current_user


@app.post("/token",response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username},expires_delta=access_token_expires)

    return {"access_token":access_token,"token":"bearer"}

@app.get("/users/me/",response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id":1,"owner": current_user}]

@app.get("/users/some")
async def some(current_user: UserInDb = Depends(get_current_active_user)):
    return {"message":"protegiendo esta ruta"}


#obtener todos los registros de la base de datos
@app.get("/data")
def data(current_user = Depends(get_current_active_user)):
    datos = objDb.getAllData()
    for dato in datos:
        dato['_id'] = str(dato['_id'])

    return {"data":datos}

#2. obtener un registro
@app.get("/data/{id}")
def dataOne(id:str, current_user = Depends(get_current_active_user)):
    try:
        data = objDb.getData(id)
        
        if isinstance(data,dict):
            data['_id']= str(data['_id'])
            return {"data":data}
        else:
            raise HTTPException(status_code=404,detail="data no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#3. ingresar un registro
@app.post("/data")
def insert_data(data:dict, current_user=Depends(get_current_active_user)):
    try:
        data['date'] = datetime.now()
        inserted = objDb.insertOne(data)

        if inserted:
            return {"message":f"Registro ingresado con el ID: {inserted}"}
        else:
            raise HTTPException(status_code=500, detail="Error al insertar el registro")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#4. Eliminar
@app.delete("/data/{id}")
def delete_data_by_id(id:str,current_user = Depends(get_current_active_user)):
    try:
        result = objDb.deleteData(id)
        if result == "Registro Eliminado":
            return {"message": result}
        elif result == "Registro no encontrado":
            raise HTTPException(status_code=404, detail="registro no encontrado")
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar el registro")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#5. Update
@app.put("/data/{id}")
def update_data_by_id(id:str,data:dict,current_user = Depends(get_current_active_user)):
    result = objDb.updateData(id,data)
    if result == "Registro actualizado con exito":
        return {"message":result}
    elif result == "Registro no encontrado":
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    else:
        raise HTTPException(status_code=500, detail="Error al actualizar el registro")


if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0",port=8000)