import os
import json
import pickle

class JsonDBManager:

    def __init__(self):
        self.jsondb_folder_path = os.path.expanduser("~/Documents/JsonDB")
        self.jsondb_sysinfo_folder_path = os.path.join(self.jsondb_folder_path, "__sysinfo__")

        if not os.path.exists(self.jsondb_folder_path):
            os.makedirs(self.jsondb_folder_path)

        if not os.path.exists(self.jsondb_sysinfo_folder_path):
            os.makedirs(self.jsondb_sysinfo_folder_path)


    def create(self, db_name: str, partition_keys: list[str], sort_keys: list[str]) -> bool:
        """Creates a new database. Initializes the database

        :param db_name str: Database name
        :param partition_keys list[str]: List of partition key names
        :param sort_keys list[str]: List of sort key names

        :return bool: Flag indicating if the creation was successful
        """

        db_sysinfo_file_path = os.path.join(
            self.jsondb_sysinfo_folder_path,
            f"{db_name}.pickle"
        )

        db_folder_path = os.path.join(
            self.jsondb_folder_path,
            db_name
        )

        if os.path.exists(db_sysinfo_file_path):
            return False
        
        if os.path.exists(db_folder_path):
            return False
        
        os.makedirs(db_folder_path)

        self.__save_db_status(
            db_name,
            {
                "partition_keys": partition_keys,
                "sort_keys": sort_keys,
                "db_partitions": []
            }
        )

        return True

    def delete(self, db_name: str) -> bool:
        """Deletes a database
        WARNING: All database data will be lost
        
        :param db_name str: Name of the database to delete
        :return bool: Flag indicating if the deletion process was succeeded
        """

        db_sysinfo_file_path = os.path.join(self.jsondb_sysinfo_folder_path, f"{db_name}.pickle")
        db_folder_path = os.path.join(self.jsondb_folder_path, db_name)

        if not os.path.exists(db_folder_path):
            return False
        
        if not os.path.exists(db_sysinfo_file_path):
            return False
        
        for db_file_name in os.listdir(db_folder_path):
            os.remove(os.path.join(db_folder_path, db_file_name))
        
        os.remove(db_sysinfo_file_path)
        os.removedirs(db_folder_path)

        return True


    def load_partition_data(self, db_name: str, partition_name: str) -> list:
        """Load a partition file and returns the items
        
        :param db_name str: Name of the database
        :param partition_name str: Name of the partition file

        :return list: partition items
        """

        partition_file_path = f"{self.jsondb_folder_path}/{db_name}/{partition_name}.json"

        if not os.path.exists(partition_file_path):
            return []
        
        with open(partition_file_path, "r+") as partition_file:
            partition_data = partition_file.read()
        
        return json.loads(partition_data)
    

    def write_partition_data(self, db_name: str, partition_name: str, data: dict) -> bool:
        """Writes data into a database partition

        :param db_name str: Name of the database
        :param partition_name str: Name of the partition file
        :param data dict: Data to write

        :return bool: Flag indicating if the writting process was succeeded
        """

        if not isinstance(data, dict):
            return False

        partition_file_path = f"{self.jsondb_folder_path}/{db_name}/{partition_name}.json"

        status = self.__load_db_status(db_name)
        if not os.path.exists(partition_file_path) and not partition_name in status["db_partitions"]:
            status["db_partitions"].append(partition_name)
            self.__save_db_status(db_name, status)

        with open(partition_file_path, "w+") as partition_file:
            partition_file.write(json.dumps(data, indent=4))
        
        return True
    
    
    def delete_partition(self, db_name: str, partition_name: str) -> bool:
        """Delete a partition
        WARNING: All the partition data will be lost

        :param db_name str: Name of the database
        :param partition_name str: Name of the file partition
        
        :return bool: Flag indicating if the process was succeeded
        """

        partition_file_path = f"{self.jsondb_folder_path}/{db_name}/{partition_name}.json"

        if not os.path.exists(partition_file_path): 
            return False

        status = self.__load_db_status(db_name)
        status["db_partitions"].remove(partition_name)
        self.__save_db_status(db_name, status)

        os.remove(partition_file_path)

        return True


    def list_databases(self) -> list:
        """List all the created databases

        :return list: List of databases
        """

        db_list = os.listdir(self.jsondb_folder_path)
        db_list.remove("__sysinfo__")

        return db_list
    

    def list_database_partitions(self, db_name: str) -> list:
        """List partitions within a database

        :param db_name str: Name of the database
        
        :return list: List of database partitions
        """

        if not self.database_exists(db_name): 
            return []

        db_status = self.__load_db_status(db_name)

        return db_status["db_partitions"]
    

    def database_exists(self, db_name: str) -> bool:
        """Checks if a database exists
        
        :param db_name str: Name of the database
        
        :return bool: Flag indicating if the database exists
        """

        db_file_path = os.path.join(self.jsondb_sysinfo_folder_path, f"{db_name}.pickle")

        if not os.path.exists(db_file_path):
            return False
        
        return True


    def database_partition_exists(self, db_name: str, partition_filename: str) -> bool:
        """Checks if a partition exists within a database

        :param db_name str: Name of the database
        :param partition_filename str: Name of the partition

        :return bool: Flag indicating if the database exists
        """
        partition_file_path = os.path.join(
            self.jsondb_folder_path,
            db_name,
            f"{partition_filename}.json"
        )

        return os.path.exists(partition_file_path)


    def get_database_partition_keys(self, db_name: str) -> list:
        """Returns database partition key list

        :param db_name str: Name of the database
        
        :return list: List containing the partition keys
        """

        if not self.database_exists(db_name):
            return []
        
        db_status = self.__load_db_status(db_name)

        return db_status["partition_keys"]
    

    def get_database_sort_keys(self, db_name: str) -> list:
        """Returns database sort key list

        :param db_name str: Name of the database
        
        :return list: List containing the sort keys
        """

        if not self.database_exists(db_name):
            return []

        db_status = self.__load_db_status(db_name)

        return db_status["sort_keys"]
        

    def __db_folder_exists(self, db_name):
        """Checks if a database folder exists (if the database was initialized)
        
        :param db_name str: Name of the database
        
        :return bool: Flag indicating if the database folder exists
        """

        db_folder_path = os.path.join(
            self.jsondb_folder_path,
            db_name
        )

        return os.path.exists(db_folder_path)
    

    def __db_status_file_exists(self, db_name: str) -> bool:
        """Check if a database status file exists (if the database was initialized)

        :param db_name str: Name of the database
        
        :return bool: Flag indicating if the database exists
        """
        
        db_status_file_path = os.path.join(
            self.jsondb_sysinfo_folder_path,
            f"{db_name}.pickle"
        )

        return os.path.exists(db_status_file_path)


    def __load_db_status(self, db_name: str) -> dict:
        """Load database status information

        :param db_name str: Name of the database

        :return dict: Database status dict
        """

        if not self.__db_status_file_exists(db_name):
            return {}
        
        db_status_file_path = os.path.join(
            self.jsondb_sysinfo_folder_path,
            f"{db_name}.pickle"
        )

        with open(db_status_file_path, "rb") as db_status_pickled:
            db_status = pickle.load(db_status_pickled)

        return db_status
    

    def __save_db_status(self, db_name: str, db_status: dict) -> bool: 
        """Overwrite status of database

        :param db_name str: Name of the database
        :param db_status dict: New database status

        :return bool: Flag indicating if the status update was succesful
        """


        db_status_file_path = os.path.join(
            self.jsondb_sysinfo_folder_path,
            f"{db_name}.pickle"
        )

        with open(db_status_file_path, "wb") as db_status_pickled:
            pickle.dump(db_status, db_status_pickled)

        return True 
        
        