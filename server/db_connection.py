from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

connection_string = ("mongodb+srv://tofuhermit:vTYsOqcDDjuvSMlD@cluster0.hd8bmua.mongodb.net/?retryWrites=true&w"
                     "=majority&appName=Cluster0")

client = MongoClient(connection_string)

# print(client.list_database_names())
#
db = client["traffic-data"]
#
print(db.list_collection_names())


def insert_traffic_data(class_type, date, in_time, out_time, full_address):
    collection = db["traffic-instances"]
    if class_type == "car" or class_type == "van":
        vehicle_type = "private"
    else:
        vehicle_type = "public"

    if in_time == None:
        in_time = out_time
    traffic_data = {
        "class": class_type,
        "type": vehicle_type,
        "date": date,
        "in_time": in_time,
        "out_time": out_time,
        "full_address": full_address
    }

    inserted_id = collection.insert_one(traffic_data).inserted_id
    inserted_id = 0
    return inserted_id


def find_traffic_data(query_params):
    collection = db["traffic-instances"]
    query = {}

    # Example: Handle a range query for a field named 'age'
    if 'date' in query_params:
        query['date'] = {'$gte': str(query_params['date'])}
        del query_params['date']

    # Add remaining query params directly to the query
    query.update(query_params)

    documents = collection.find(query)
    return documents
# print(list(collection.find()))
# print(insert_traffic_data("Car", "PUV", "00:00:00", "00:01:32", "San Jose del Monte"))
