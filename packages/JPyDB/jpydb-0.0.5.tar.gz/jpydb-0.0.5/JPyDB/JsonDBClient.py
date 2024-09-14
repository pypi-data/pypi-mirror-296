from flask import Flask, request
from JPyDB.JsonDB import JsonDB
from JPyDB.JsonDBManager import JsonDBManager
import argparse
import sys

app = Flask(__name__)
json_db_client = JsonDB()
json_db_manager = JsonDBManager()


@app.route("/get_items", methods=["GET"])
def get_items():
    db_name = request.args.get("db_name")
    
    return json_db_client.get_items(db_name)


@app.route("/put_items", methods=["PUT"])
def put_items():
    db_name = request.args.get("db_name")
    items = request.get_json()
    
    return str(json_db_client.put_items(db_name, items))


@app.route("/query_items", methods=["POST"])
def query_items():
    db_name = request.args.get("db_name")
    query_list = request.get_json()

    return json_db_client.query_items(db_name, query_list)


@app.route("/delete_items", methods=["POST"])
def delete_items():
    db_name = request.args.get("db_name")
    query_list = request.get_json()

    return str(json_db_client.delete_items(db_name, query_list))


@app.route("/create", methods=["POST"])
def create():
    db_name = request.args.get("db_name")
    db_keys = request.get_json()

    return str(json_db_manager.create(db_name, **db_keys))


@app.route("/delete", methods=["GET"])
def delete():
    db_name = request.args.get("db_name")

    return str(json_db_manager.delete(db_name))


@app.route("/list_databases", methods=["GET"])
def get_databases():
    return json_db_manager.list_databases()

def main():

    if len(sys.argv) < 1:
        print("No port specified")
        sys.exit(0)


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        "-p",
        type = int,
        default = 10000,
        help = "Port number by default port 10000 will be used"
    )

    args = parser.parse_args().__dict__

    app.run(
        host="localhost",
        port=args["port"]
    )