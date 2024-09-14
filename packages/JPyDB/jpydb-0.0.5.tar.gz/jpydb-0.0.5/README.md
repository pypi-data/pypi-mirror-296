## JPyDB

### Introduction
JPyDB is a python library developed by Manuel Sánchez Mascarell.

The main purpose of this library is to create and manage NoSQL databases in you local machine. This database uses JSON files for store the data.

The idea behing `JPyDB` was to make something similar to AWS DynamoDB resource but for local developments, being useful for develop own projects without requiring a cloud environment.

### Basic usage

In the library we can find two main modules `JsonDB` and `JsonDBManager`.

The first one `JsonDB` is used to interact with the data, here, we can find functions like (put_items, get_items, query_items, delete_items, ...).

By other hand the `JsonDBManager` is used to manage databases (create, delete, ...)

Internally, `JsonDB` makes use of the `JsonDBManager` module for making checks if the database exists, getting the information of the database, and so on.

#### Library imports

```python
from JPyDB.JsonDB import JsonDB
from JPyDB.JsonDBManager import JsonDBManager

json_db_client = JsonDB()
json_db_manager = JsonDBManager()
```

#### Database creation

For create a new fresh database, we will make usage of the `.create()` method from the `JsonDBManager` module.

For creating a new databas, we will need three **mandatory** arguments:
- `db_name`: how the new database will be named.
- `partition_keys`: list containing the name of the fields used to partition the data.
- `sort_keys`: list containing the name of the fields used to index the data.


```python
    # json_db_manager.create(<db_name>, <partition_keys>, <sort_keys>)
    json_db_manager.create("clients", ["clientId"], ["purchaseId"])
```

This method will return a boolean flag for indicate if the creation process was succeeded or not.

If the creation was as expected, now, we will see a folder structure on the following path: _~/Documents/JsonDB_

You will find something like this:

```bash
C:\Users\<usr>\Documents
├───...
├───JsonDB
│   ├───clients
│   └───__sysinfo__
└───...
```

In the folder `clients` you will find all the data and the partitions of your database. Meanwhile the `__sysinfo__` contains all the metadata of the database (partition keys, sort keys, ...).

**NOTE:** clients folder won't be created until you don't add an item to the database

#### Adding items

For interact with the data, we will make use of the `JsonDB` module, this, will allow us to add new items, and query them.

For achieve this, we will make use of two methods, the `.put_items()` for add an item into the database and the `.get_items()` for retrieve it.


```python 
item = {
    "clientId": "001",
    "purchaseId": "001",
    "purchasedItems": {
        "itm01": 3,
        "itm02": 4
    }
}

#json_db_client.put_item(<db_name>, <item>)
json_db_client.put_item("clients", item)
```

This will return a flag indicating if the insertion process was succeeded. Something to have on mind is that actually the put_items method **works like an upsert**, if the item is found, it will update it, otherwise, it will insert the data as a new item.

Now, we will retrieve the item, for achieve that, we will use the `.get_items()` method, this method retrieves all the items stored inside the database.\
Another solution could be using the `.query_items()`, but we will go throught this method afterwards.

```python
#json_db_client.get_items(<db_name>)
json_db_client.get_items('clients')
```

The database now should return the item, we've stored previously (if the database doesn't contain any item, it will return an empty list).

```python
{
    "clientId": "001",
    "purchaseId": "001",
    "purchasedItems": {
        "itm01": 3,
        "itm02": 4
    }
}
```

### Managing databases

#### List databases

In addition to the `.create()` method that we've reviewed before, the `JsonDBManager` contains more methods for managing our databases.

The `.list_databases()` method allow us to list all the created and available databases.

```python
#json_db_manager.list_databases()
json_db_manager.list_databases()
```

This will return a list of the available databases. In our case, it appears the clients database that we've created before.

```bash
["clients"]
```

#### List database partitions
The `JsonDBManager` module also allows you to list database partitions using the `.list_database_partitions()` method, this usually is used more often for internal purposes.

```python
#json_db_manager.list_database_partitions(db_name)
json_db_manager.list_database_partitions("clients")
```

The output is also a list containing the partitions of the specified database, in our example, when adding the item, the system has created a new partition to store the client's data.

```bash
["clientId=001"]
```

#### Delete database
The `JsonDBManager` module also contains a `.delete()` method, this method is used to delete databases.

**NOTE:** Use this method if you understand what you're doing, if not, you may lose all your data.

```python
#json_db_manager.delete(<db_name>)
json_db_manager.delete("clients")
```

#### Delete database partition
`JsonDBManager` also allows you to only remove an specific partition of data, for achieve that, you may use the  `.delete_partition()` method. This method **isn't recommended** for being used, we encourage to use the `.delete_items()` from the `JsonDB` module.

**NOTE:** Use this method if you understand what you're doing, if not, you may lose all your data.

```python
#json_db_manager.delete_partition(<db_name>, <partition_name>)
json_db_manager.delete_partition("clients", "clientId=001")
```

#### Check if a database exists
For check if a database is already created or exists, `JsonDBManager` implements a method called `.database_exists()` this will return a flag indicating if the specified database exists.

```python
# json_db_client.database_exists(<db_name>)
json_db_client.database_exists("clients")
```

#### Check if a partition exists within a database
For check if a partition exists inside a database, the `JsonDBManager` module, implements the method called `.database_partition_exists()`, this will return a flag indicating if the partition exists within the database

```python
# json_db_manager.database_partition_exists(<db_name>, <partition_name>)
json_db_manager.database_partition_exists("clients", "client=001")
```

### Managing database data

#### Querying data
You can query your database items using the method `.query_items()` from the `JsonDB` module. This method expects a list of queries, the method will return those items who match with the specified attributes.

```python
# json_db_client.query_items(<db_name>, <query_list>)
json_db_client.query_items("clients", [{"clientId": "001"}])
```

#### Delete items
You can also delete some specific items, for achieve that, we will make use of the `.delete_items()` method, from the `JsonDB` module. This will allow us to only delete those items who match with the specified query.

```python
#json_db_client.delete_items(<db_name>, <query_list>)
json_db_client.delete_items("clients", [{"clientId": "001"}])
```

**NOTE:** Use this method if you understand what you're doing, if not, you may lose all your data.

## JPyDB Server
There's a third module in the package, this is the `JsonDBClient`, this module contains a server implementation using `flask` module.

For launch your own server, please execute:
```bash
jsondbclient
```

You can use the --port, -p argument to change the port (by default uses the port 10000). you can make all the basic functions from the created server, like, get_itemms, query_items, create databases, this is the list of the included methods:
- [GET] - https://localhost:10000/get_items?db_name=<db_name>
- [PUT] - https://localhost:10000/put_items?db_name=<db_name>
- [POST] - https://localhost:10000/query_items?db_name=<db_name>
- [POST] - https://localhost:10000/delete_items?db_name=<db_name>
- [POST] - https://localhost:10000/create?db_name=<db_name>
- [GET] - https://localhost:10000/delete?db_name=<db_name>
- [GET] - https://localhost:10000/list_databases?db_name=<db_name>

