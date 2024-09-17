from JPyDB import JPyDBClient, JPyDBManager

def test_create_table():

    print("### Testing database creation ###")
    json_db_manager = JPyDBManager()

    print("executing case 01...")
    test01 = json_db_manager.create_table("pytest_table01", partition_keys=["pk"], sort_keys=["sk"])
    assert test01 == True
    
    print("executing case 02...")
    test02 = json_db_manager.create_table("pytest_table02", partition_keys=["pk01", "pk02"], sort_keys=["sk"])
    assert test02 == True
    
    print("executing case 03...")
    test03 = json_db_manager.create_table("pytest_table03", partition_keys=["pk"], sort_keys=["sk01", "sk02"])
    assert test03 == True
      
    print("executing case 04...")
    test04 = json_db_manager.create_table("pytest_table04", partition_keys=["pk"], sort_keys=None)
    assert test04 == False
    
    print("executing case 05...")
    test05 = json_db_manager.create_table("pytest_table05", partition_keys=None, sort_keys=["sk"])
    assert test05 == False
    
    print("executing case 06...")
    test06 = json_db_manager.create_table("pytest_table05", partition_keys="pk", sort_keys=["sk"])
    assert test06 == False
    
    print("executing case 07...")
    test07 = json_db_manager.create_table("pytest_table05", partition_keys=["pk"], sort_keys="sk")
    assert test07 == False

def test_put_items():

    print("### Testing data insetion ###")
    json_db_client = JPyDBClient()

    print("executing case 01...")    
    test01 = json_db_client.put_items("pytest_table01", [{"pk": 0, "sk": 1}, {"pk": 1, "sk": 0}, {"pk": 2, "sk": 0}, {"pk": 2, "sk": 1, "a": 0}, {"pk": 0, "sk": 1, "b": 3}])
    assert test01 == True

    print("executing case 02...")    
    test02 = json_db_client.put_items("pytest_table01", {"pk": 0, "sk": 3, "a": 1, "b": 2})
    assert test02 == True
    
    print("executing case 03...")    
    test03 = json_db_client.put_items("pytest_table01", {"a": 0, "b": 1})
    assert test03 == False

    print("executing case 04...")
    test04 = json_db_client.put_items("table_not_found", {"pk": 0, "sk": 1})
    assert test04 == False

    print("executing case 05...")
    test05 = json_db_client.put_items("pytest_table02", {"pk01": 0, "sk": 1})
    assert test05 == False

    print("executing case 06...")
    test06 = json_db_client.put_items("pytest_table02", {"pk01": 0, "pk02": 1, "sk": 1})
    assert test06 == True

    print("executing case 07...")
    test07 = json_db_client.put_items("pytest_table02", {"pk01": 0, "pk02": 1, "a": 1})
    assert test07 == False


def test_query_items():

    print("### Testing queries ###")
    json_db_client = JPyDBClient()    

    print("executing case 01...")
    test = json_db_client.query_items("pytest_table01", [{}])
    assert test != []

    print("executing case 02...")
    test = json_db_client.query_items("pytest_table01", [{"x": 0}])
    assert test == []

    print("executing case 03...")
    test = json_db_client.query_items("pytest_table01", [{"pk": 1, "sk": 0}])
    assert test != []

    print("executing case 04...")
    test = json_db_client.query_items("pytest_table01", [{"a": 1}])
    assert test != []

    print("executing case 05")
    test = json_db_client.query_items("pytest_table01", {"a": 1})
    assert test == []

    print("executing case 06")    
    test = json_db_client.query_items("pytest_table01", None)
    assert test == []

    print("executing case 07")    
    test = json_db_client.query_items("pytest_table01", "a=0")
    assert test == []

    print("executing case 08")    
    test = json_db_client.query_items("pytest_table01", "pk=0,sk=0")
    assert test == []

    print("executing case 09")    
    test = json_db_client.query_items("pytest_table01", True)
    assert test == []

    print("executing case 10")    
    test = json_db_client.query_items("pytest_table01", [{"pk": 0}, "a=0"])
    assert test == []
    
def test_get_items():
    
    print("### Test Geting items ###")
    json_db_manager = JPyDBManager()
    json_db_client = JPyDBClient()

    print("executing case 01...")
    test = json_db_client.get_items("pytest_table01")
    assert test != []

    print("executing case 02...")
    test = json_db_client.get_items("pytest_table02")
    assert test != []
    
    print("executing case 03...")
    test = json_db_client.get_items("pytest_table03")
    assert test == []
    
    print("executing case 04...")
    test = json_db_client.get_items("table_not_found")
    assert test == []

    print("executing case 05...")
    test = json_db_client.get_items(None)
    assert test == []


def test_delete_item():

    print("### Testing item deleting ###")
    json_db_manager = JPyDBManager()
    json_db_client = JPyDBClient()

    print("executing case 01...")
    test = json_db_client.delete_items("pytest_table01", [{"a": 0, "b": 0}])
    assert test == True

    print("executing case 02...")
    test = json_db_client.delete_items("pytest_table01", [{}])
    assert test == True

    print("executing case 02-bis...")
    test = json_db_client.get_items("pytest_table01")
    assert test == []

    print("executing case 02-bis-bis...")
    test = json_db_manager.table_exists("pytest_table01")
    assert test == True

    print("executing case 03...")
    test = json_db_client.delete_items("pytest_table02", [{"pk": 1}, {"pk": 2}])
    assert test == True
    
    print("executing case 04...")
    test = json_db_client.delete_items("pytest_table02", "test")
    assert test == False

    print("executing case 05...")
    test = json_db_client.delete_items("pytest_table02", None)
    assert test == False

    print("executing case 06...")
    test = json_db_client.delete_items("pytest_table02", [{"pk": 1}, {"pk": 2}, "hola"])
    assert test == False

def test_delete_table():
    print("### Test table removal ###")
    json_db_manager = JPyDBManager()

    print("executing pre-case 01...")
    test = json_db_manager.table_exists("pytest_table01")
    assert test == True    

    print("executing case 01...")
    test = json_db_manager.delete_table("pytest_table01")
    assert test == True

    print("executing post-case 01...")
    test = json_db_manager.table_exists("pytest_table01")
    assert test == False
     
    print("executing case 02...")
    test = json_db_manager.delete_table(["pytest_table02", "pytest_table03"])
    assert test == False

    print("executing case 03...")
    test = json_db_manager.delete_table("pytest_table02")
    assert test == True

    print("executing case 04...")
    test = json_db_manager.delete_table("pytest_table03")
    assert test == True

    print("executing case 05...")
    test = json_db_manager.delete_table("pytest_table03")
    assert test == False

    print("executing case 06...")
    test = json_db_manager.delete_table("table_not_found")
    assert test == False

    print("executing case 07...")
    test = json_db_manager.delete_table(None)
    assert test == False

    print("executing case 08...")
    test = json_db_manager.delete_table(True)
    assert test == False