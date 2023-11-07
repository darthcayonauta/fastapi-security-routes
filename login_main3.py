'''
la clave de usuario es : 'tim1234'
'''

import httpx
import asyncio

credentials = {
    "username":"tim",
    "password": "tim1234"
}

#url del token
auth_url="http://localhost:8000/token"

#info del user
user_info_url = "http://localhost:8000/users/me/"
user_items_url = "http://localhost:8000/users/me/items"
some_url = "http://localhost:8000/users/some"

#funcion de obtener data del token
async def get_access_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(auth_url,data=credentials)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            return access_token
        else:
            print(f"Error al autenticarse: {response.status_code}, {response.text}")

#informacion del access_token     
access_token =  asyncio.run( get_access_token())

#accesos a rutas protegidas
async def get_protected_data(url):
    headers ={
        "Authorization":f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url,headers=headers)
        if response.status_code==200:
            data = response.json()
            return data
        else:
            print(f"Error al obtener datos: {response.status_code}, {response.text}")

if access_token:
    print(f"Token de acceso obtenido: {access_token}")

user_info = asyncio.run(get_protected_data(user_info_url))
user_items = asyncio.run(get_protected_data(user_items_url))
some_data = asyncio.run(get_protected_data(some_url))

if user_info:
    print("Datos de usuario:")
    print(user_info)

if user_items:
    print("Datos de elementos de usuario:")
    print(user_items)

if some_url:
    print(f"Datos de ruta protegida '{some_url}'")
    print(some_data)