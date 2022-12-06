import datetime as dt
import pymongo
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
from bson import json_util, ObjectId, timestamp
from flask import Flask, request, jsonify
from flask_objectid_converter import ObjectIDConverter
from Schemas import GreenHouseInfoSchemaPost
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
import os

MONGODB_LINK = os.environ.get("MONGODB_LINK")
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASS = os.environ.get("MONGODB_PASS")



app = Flask(__name__)

client = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_LINK}/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.GreenHouseDB

app.config['DEBUG'] = True



app.url_map.converters['objectid'] = ObjectIDConverter


if 'instanceData' not in db.list_collection_names():
    db.create_collection("instanceData",
                         timeseries={'timeField': 'time', 'metaField': 'greenhouseId', 'granularity': 'minutes'})


@app.route("/")
def index():
    return "hi <br> you should try http://127.0.0.1:5000/greenhouses/{greenhouseId} instead"

@app.route("/greenhouses/<int:greenhouseId>", methods=["GET"])
def get_all_greenhouse_info(greenhouseId):
    try:
        cursor = db.instanceData.find({"greenhouseId": greenhouseId})
        instances = list(cursor)
        for instance in instances:
            if "_id" in instance:
                instance["_id"] = str(instance["_id"])

        return jsonify(instances)

    except Exception as e:
        print(e)
        return {"error" : "some error happened"}, 501

@app.route("/greenhouses/<int:greenhouseId>", methods=["POST"])
def add_greenhouse_info(greenhouseId:int):
    instance = request.json
    instance["greenhouseId"] = greenhouseId

    error = GreenHouseInfoSchemaPost().validate(request.json)
    if error:
        return error, 400


    instance["time"] = dt.datetime.today().replace(microsecond=0)
    print(instance["time"])



    try:
        inserted_id = db.instanceData.insert_one(instance).inserted_id
        instance["_id"] = str(inserted_id)
        return jsonify(instance)
    except Exception as e:
        print(e)
        return {"error": "some error happened"}, 501

@app.route("/greenhouses/<int:greenhouseId>/time", methods=["GET"])
def get_greenhouse_info_by_time(greenhouseId):

    start = request.args.get("start")
    end = request.args.get("end")

    try:
        end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    except Exception as e:
        return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400


    docs = list(db.instanceData.aggregate([
                {"$match" : {"time": {"$gt" : start}}},
                {"$project":
                     {"greenhouseId": greenhouseId, "humidity": "$humidity", "temp": "$temp", "lumens":"$lumens"}
                 }
        ]))

    for doc in docs:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])

    return docs



if __name__ == "__main__":
    app.run()