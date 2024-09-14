from bson import ObjectId
from pymongo import MongoClient


class DBConnection:

    @staticmethod
    def get_testdata_from_mongoDB(db_connection, table_name,col_name,id):
        client = MongoClient(db_connection)
        dbName = client[table_name]
        collection_name = dbName[col_name]
        records = collection_name.find_one({"_id":ObjectId(id)})
        return records

    @staticmethod
    def get_safety_testdata_from_mongoDB(db_connection, table_name, col_name, id, test_case_id):
        client = MongoClient(db_connection)
        dbName = client.get_database(table_name)
        collection_name = dbName.get_collection(col_name)
        records = collection_name.find_one({"vault_id": ObjectId(id), "tag_id": test_case_id})
        return records


