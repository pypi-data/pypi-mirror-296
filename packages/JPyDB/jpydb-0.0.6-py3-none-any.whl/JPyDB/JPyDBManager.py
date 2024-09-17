import os
import json
import pickle

class JPyDBManager:

    def __init__(self):
        self.jpydb_folder_path = os.path.expanduser("~/Documents/JPyDB")
        self.jpydb_sysinfo_folder_path = os.path.join(self.jpydb_folder_path, "__sysinfo__")
        self.jpydb_export_folder_path = os.path.join(self.jpydb_folder_path, "__exports__")

        if not os.path.exists(self.jpydb_folder_path):
            os.makedirs(self.jpydb_folder_path)

        if not os.path.exists(self.jpydb_sysinfo_folder_path):
            os.makedirs(self.jpydb_sysinfo_folder_path)


    def create_table(self, table_name: str, partition_keys: list[str], sort_keys: list[str]) -> bool:
        """Creates a new table. Initializes the table

        :param table_name str: table name
        :param partition_keys list[str]: List of partition key names
        :param sort_keys list[str]: List of sort key names

        :return bool: Flag indicating if the creation was successful
        """

        if not partition_keys: return False
        if not isinstance(partition_keys, list): return False

        if not sort_keys: return False
        if not isinstance(sort_keys, list): return False

        if table_name.startswith("__") or table_name.endswith("__"): return False

        db_sysinfo_file_path = os.path.join(
            self.jpydb_sysinfo_folder_path,
            f"{table_name}.pickle"
        )

        db_folder_path = os.path.join(
            self.jpydb_folder_path,
            table_name
        )

        if os.path.exists(db_sysinfo_file_path):
            return False
        
        if os.path.exists(db_folder_path):
            return False

        os.makedirs(db_folder_path)

        self.__save_db_status(
            table_name,
            {
                "partition_keys": partition_keys,
                "sort_keys": sort_keys,
                "db_partitions": []
            }
        )

        return True

    def delete_table(self, table_name: str) -> bool:
        """Deletes a table
        WARNING: All table data will be lost
        
        :param table_name str: Name of the table to delete
        :return bool: Flag indicating if the deletion process was succeeded
        """
        if not isinstance(table_name, str): return False
        if table_name.startswith("__") or table_name.endswith("__"): return False

        db_sysinfo_file_path = os.path.join(self.jpydb_sysinfo_folder_path, f"{table_name}.pickle")
        db_folder_path = os.path.join(self.jpydb_folder_path, table_name)

        if not os.path.exists(db_folder_path):
            return False
        
        if not os.path.exists(db_sysinfo_file_path):
            return False
        
        for db_file_name in os.listdir(db_folder_path):
            os.remove(os.path.join(db_folder_path, db_file_name))
        
        os.remove(db_sysinfo_file_path)
        os.removedirs(db_folder_path)

        return True
    

    def load_partition_data(self, table_name: str, partition_name: str) -> list:
        """Load a partition file and returns the items
        
        :param table_name str: Name of the table
        :param partition_name str: Name of the partition file

        :return list: partition items
        """

        partition_file_path = f"{self.jpydb_folder_path}/{table_name}/{partition_name}.json"

        if not os.path.exists(partition_file_path):
            return []
        
        with open(partition_file_path, "r+") as partition_file:
            partition_data = partition_file.read()
        
        return json.loads(partition_data)
    

    def write_partition_data(self, table_name: str, partition_name: str, data: dict) -> bool:
        """Writes data into a table partition

        :param table_name str: Name of the table
        :param partition_name str: Name of the partition file
        :param data dict: Data to write

        :return bool: Flag indicating if the writting process was succeeded
        """

        if not isinstance(data, dict):
            return False

        partition_file_path = f"{self.jpydb_folder_path}/{table_name}/{partition_name}.json"

        status = self.__load_db_status(table_name)
        if not os.path.exists(partition_file_path) and not partition_name in status["db_partitions"]:
            status["db_partitions"].append(partition_name)
            self.__save_db_status(table_name, status)

        with open(partition_file_path, "w+") as partition_file:
            partition_file.write(json.dumps(data, indent=4))
        
        return True
    
    
    def delete_partition(self, table_name: str, partition_name: str) -> bool:
        """Delete a partition
        WARNING: All the partition data will be lost

        :param table_name str: Name of the table
        :param partition_name str: Name of the file partition
        
        :return bool: Flag indicating if the process was succeeded
        """

        partition_file_path = f"{self.jpydb_folder_path}/{table_name}/{partition_name}.json"

        if not os.path.exists(partition_file_path): 
            return False

        status = self.__load_db_status(table_name)
        status["db_partitions"].remove(partition_name)
        self.__save_db_status(table_name, status)

        os.remove(partition_file_path)

        return True


    def list_tables(self) -> list:
        """List all the created tables

        :return list: List of tables
        """

        db_list = os.listdir(self.jpydb_folder_path)
        for db_name in db_list:
            if db_name.startswith("__") or db_name.endswith("__"):
                db_list.remove(db_name)

        return db_list
    

    def list_table_partitions(self, table_name: str) -> list:
        """List partitions within a table

        :param table_name str: Name of the table
        
        :return list: List of table partitions
        """

        if not self.table_exists(table_name): 
            return []

        db_status = self.__load_db_status(table_name)

        return db_status["db_partitions"]
    

    def table_exists(self, table_name: str) -> bool:
        """Checks if a table exists
        
        :param table_name str: Name of the table
        
        :return bool: Flag indicating if the table exists
        """

        db_file_path = os.path.join(self.jpydb_sysinfo_folder_path, f"{table_name}.pickle")

        if not os.path.exists(db_file_path):
            return False
        
        return True


    def table_partition_exists(self, table_name: str, partition_filename: str) -> bool:
        """Checks if a partition exists within a table

        :param table_name str: Name of the table
        :param partition_filename str: Name of the partition

        :return bool: Flag indicating if the table exists
        """
        partition_file_path = os.path.join(
            self.jpydb_folder_path,
            table_name,
            f"{partition_filename}.json"
        )

        return os.path.exists(partition_file_path)


    def get_table_partition_keys(self, table_name: str) -> list:
        """Returns table partition key list

        :param table_name str: Name of the table
        
        :return list: List containing the partition keys
        """

        if not self.table_exists(table_name):
            return []
        
        db_status = self.__load_db_status(table_name)

        return db_status["partition_keys"]
    

    def get_table_sort_keys(self, table_name: str) -> list:
        """Returns table sort key list

        :param table_name str: Name of the table
        
        :return list: List containing the sort keys
        """

        if not self.table_exists(table_name):
            return []

        db_status = self.__load_db_status(table_name)

        return db_status["sort_keys"]
        

    def __db_folder_exists(self, table_name):
        """Checks if a table folder exists (if the table was initialized)
        
        :param table_name str: Name of the table
        
        :return bool: Flag indicating if the table folder exists
        """

        db_folder_path = os.path.join(
            self.jpydb_folder_path,
            table_name
        )

        return os.path.exists(db_folder_path)
    

    def __db_status_file_exists(self, table_name: str) -> bool:
        """Check if a table status file exists (if the table was initialized)

        :param table_name str: Name of the table
        
        :return bool: Flag indicating if the table exists
        """
        
        db_status_file_path = os.path.join(
            self.jpydb_sysinfo_folder_path,
            f"{table_name}.pickle"
        )

        return os.path.exists(db_status_file_path)


    def __load_db_status(self, table_name: str) -> dict:
        """Load table status information

        :param table_name str: Name of the table

        :return dict: table status dict
        """

        if not self.__db_status_file_exists(table_name):
            return {}
        
        db_status_file_path = os.path.join(
            self.jpydb_sysinfo_folder_path,
            f"{table_name}.pickle"
        )

        with open(db_status_file_path, "rb") as db_status_pickled:
            db_status = pickle.load(db_status_pickled)

        return db_status
    

    def __save_db_status(self, table_name: str, db_status: dict) -> bool: 
        """Overwrite status of table

        :param table_name str: Name of the table
        :param db_status dict: New table status

        :return bool: Flag indicating if the status update was succesful
        """


        db_status_file_path = os.path.join(
            self.jpydb_sysinfo_folder_path,
            f"{table_name}.pickle"
        )

        with open(db_status_file_path, "wb") as db_status_pickled:
            pickle.dump(db_status, db_status_pickled)

        return True 
        
        