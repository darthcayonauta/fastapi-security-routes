'''en el ejemplo sólo usaré 1 tabla'''

from pymongo import MongoClient
from datetime import datetime
from pymongo.errors import PyMongoError
from bson import ObjectId

class Db:
    def __init__(self,mongo_host="127.0.0.1"):
        CONNECTION_STRING=f"mongodb://{mongo_host}:27017/stuffs"
        self.client = MongoClient(CONNECTION_STRING)
        #SOLO USARE 1 COLECCION, POR LO QUE LA DFINO ACA...
        self.collection = self.client['stuffs']['stuffs']

    #obtención de todos los registros
    def getAllData(self):
        data = list(self.collection.find())
        return data
    
    #obtencion de 1 solo registro
    def getData(self,id):
        data = self.collection.find_one({"_id":ObjectId(id)})
        if data:
            return data
        else:
            return {}

    #insertamos varios registros
    def insertManyData(self,data_list):
        try:
            for data in data_list:
                data['date'] = datetime.now()

            result = self.collection.insert_many(data_list)
            return result.inserted_ids
        except PyMongoError as e:
            print(f"Error al intentar ingresar datos:{e}")
            return None

    #insertamos de a 1 registro
    def insertOne(self,data):
        try:
            data['date'] = datetime.now()
            result = self.collection.insert_one(data)
            return result.inserted_id
        except PyMongoError as e:
            print(f"Error a tratar de ingresar registro: {e}")
            return None

    #eliminar un registro
    def deleteData(self,id):
        try:
            result = self.collection.delete_one({"_id":ObjectId(id)})
            if result.deleted_count > 0:
                return "Registro Eliminado"
            else:
                return "Registro no encontrado"

        except PyMongoError as e:
            print("Error al eliminar registro: {e}")
            return None
        
    #actualizar un registro
    def updateData(self,id,update_data):
        try:
            result = self.collection.update_one({"_id":ObjectId(id)},{"$set":update_data})
            if result.modified_count > 0:
                return "Registro actualizado con exito"
            else:
                return "Registro no encontrado"
        except PyMongoError as e:
            print(f"Error al actualizar el registro: {e}")
            return None
        
