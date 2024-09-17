from flask import Flask, request
from JPyDB.JPyDBClient import JPyDBClient
from JPyDB.JPyDBManager import JPyDBManager
import argparse
import sys

app = Flask(__name__)
json_db_client = JPyDBClient()
json_db_manager = JPyDBManager()


@app.route("/get_items", methods=["GET"])
def get_items():
    table_name = request.args.get("table_name")
    
    return json_db_client.get_items(table_name)


@app.route("/put_items", methods=["PUT"])
def put_items():
    table_name = request.args.get("table_name")
    items = request.get_json()
    
    return str(json_db_client.put_items(table_name, items))


@app.route("/query_items", methods=["POST"])
def query_items():
    table_name = request.args.get("table_name")
    query_list = request.get_json()

    return json_db_client.query_items(table_name, query_list)


@app.route("/delete_items", methods=["POST"])
def delete_items():
    table_name = request.args.get("table_name")
    query_list = request.get_json()

    return str(json_db_client.delete_items(table_name, query_list))


@app.route("/create_table", methods=["POST"])
def create():
    table_name = request.args.get("table_name")
    table_keys = request.get_json()

    return str(json_db_manager.create_table(table_name, **table_keys))


@app.route("/delete_table", methods=["GET"])
def delete():
    table_name = request.args.get("table_name")

    return str(json_db_manager.delete_table(table_name))


@app.route("/list_tables", methods=["GET"])
def get_tables():
    return json_db_manager.list_tables()

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