import pymongo
import json



with open("private.json","r") as f:
    file = json.load(f)
user = file["user"]
passwd = file["passwd"]




class mongo_class:
    def __init__(self):
        self.user = user
        self.password = passwd
        self.url = "mongodb+srv://{}:{}@cluster0.uggc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(self.user,self.password)


    def create_conn_to_db(self):
        try:
            conn = pymongo.MongoClient(self.url)
            return conn

        except Exception as e:
            raise e


    def close_conn(self,conn):
        try:
            conn.close()
        except Exception as e:
            raise e



    def insert_one_record(self,record_dict,db_name,col_name):
        try:
            conn = self.create_conn_to_db()
            db_obj = conn[db_name]
            col_obj = db_obj[col_name]
            col_obj.insert_one(record_dict)
            self.close_conn(conn)

        except Exception as e:
            raise e

