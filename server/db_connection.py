from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

connection_string = ("mongodb+srv://tofuhermit:vTYsOqcDDjuvSMlD@cluster0.hd8bmua.mongodb.net/?retryWrites=true&w"
                     "=majority&appName=Cluster0")

# client = MongoClient(connection_string)

# print(client.list_database_names())
#
# db = client["traffic-data"]
#
# print(db.list_collection_names())


def insert_traffic_data(class_type, in_time, out_time, full_address, vehicle_type="public"):
    return
#     if class_type == "car" or class_type == "van":
#         vehicle_type = "private"
#     collection = db.trafficinstances
#     traffic_data = {
#         "class": class_type,
#         "type": vehicle_type,
#         "in_time": in_time,
#         "out_time": out_time,
#         "full_address": full_address
#     }
#     # inserted_id = collection.insert_one(traffic_data).inserted_id


# print(insert_traffic_data("Car", "PUV", "00:00:00", "00:01:32", "San Jose del Monte"))
