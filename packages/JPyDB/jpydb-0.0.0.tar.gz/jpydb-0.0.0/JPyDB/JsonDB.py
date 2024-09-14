import os
from JPyDB.JsonDBManager import JsonDBManager


class JsonDB:

    def __init__(self): 
        self.db_manager = JsonDBManager()


    def get_items(self, db_name): 
        """Returns all database items

        :param db_name str: Name of the database

        :return list[dict]: List of database items
        """ 
        
        items = []

        for partition_name in self.db_manager.list_database_partitions(db_name):
            items = [*items, *self.db_manager.load_partition_data(db_name, partition_name).values()]

        return items
    

    def put_items(self, db_name, items):
        """Upserts items in the database

        :param db_name str: Name of the database
        :param items list|dict: List of items or item to insert
        
        :return bool: Flag indicating if the process was succeeded
        """

        partition_keys = self.db_manager.get_database_partition_keys(db_name)
        sort_keys = self.db_manager.get_database_sort_keys(db_name)

        if isinstance(items, dict):

            partition_filename = self.__get_partition_filename(partition_keys, items)
            sort_index = self.__get_sort_index(sort_keys, items)
            partition_data = {sort_index: items}
            if self.db_manager.database_partition_exists(db_name, partition_filename):
                
                partition_data = self.db_manager.load_partition_data(db_name, partition_filename)
                partition_data[sort_index] = items

            self.db_manager.write_partition_data(db_name, partition_filename, partition_data)

        elif isinstance(items, list):

            for item in items:
                partition_filename = self.__get_partition_filename(partition_keys, item)
                sort_index = self.__get_sort_index(sort_keys, item)

            
                partition_data = {sort_index: item}
                if self.db_manager.database_partition_exists(db_name, partition_filename):

                    partition_data = self.db_manager.load_partition_data(db_name, partition_filename)
                    partition_data[sort_index] = item

                self.db_manager.write_partition_data(db_name, partition_filename, partition_data)

        return True


    def query_items(self, db_name, query_list):
        """Search for similar items into a database

        :param db_name str: Name of the database
        :param query_list list[dict]: List of items to search 
        
        :return list: List of found items 
        """

        items = []

        db_partition_keys = self.db_manager.get_database_partition_keys(db_name)
        db_sort_keys = self.db_manager.get_database_sort_keys(db_name)

        for query in query_list:

            partition_filename = self.__get_partition_filename(
                db_partition_keys,
                query
            )

            sort_key_name = self.__get_sort_index(
                db_sort_keys,
                query
            )

            if partition_filename:
                partition_data = self.db_manager.load_partition_data(db_name, partition_filename)
                if not partition_data: continue

                if sort_key_name and sort_key_name in partition_data:
                    partition_item = partition_data[sort_key_name]
                    is_valid = True

                    for attr_key, attr_value in query.items():
                        if attr_key not in partition_item: is_valid = False; break
                        if partition_item[attr_key] != attr_value: is_valid = False; break

                    if is_valid: items.append(partition_item)

                elif not sort_key_name:
                    for partition_item in partition_data.values():
                        is_valid = True

                        for attr_key, attr_value in query.items():
                            if attr_key not in partition_item: is_valid = False; break
                            if partition_item[attr_key] != attr_value: is_valid = False; break

                        if is_valid: items.append(partition_item)

            else:
                for partition_name in self.db_manager.list_database_partitions(db_name):
                    partition_data = self.db_manager.load_partition_data(db_name, partition_name)
                    if not partition_data: continue

                    if sort_key_name and sort_key_name in partition_data:
                        partition_item = partition_data[sort_key_name]
                        is_valid = True

                        for attr_key, attr_value in query.items():
                            if attr_key not in partition_item: is_valid = False; break
                            if partition_item[attr_key] != attr_value: is_valid = False; break

                        if is_valid: items.append(partition_item)

                    elif not sort_key_name:
                        for partition_item in partition_data.values():
                            is_valid = True

                            for attr_key, attr_value in query.items():
                                if attr_key not in partition_item: is_valid = False; break
                                if partition_item[attr_key] != attr_value: is_valid = False; break

                            if is_valid: items.append(partition_item)
        
        return items
    

    def delete_items(self, db_name, query_list):
        """Deletes similar items into a database 

        :param db_name str: Name of the database
        :param query_list list[dict]: List of items to delete

        :return bool: Flag indicating if the process was succeeded
        """

        sort_keys_to_delete = []

        db_partition_keys = self.db_manager.get_database_partition_keys(db_name)
        db_sort_keys = self.db_manager.get_database_sort_keys(db_name)

        for query in query_list:

            partition_filename = self.__get_partition_filename(
                db_partition_keys,
                query
            )

            sort_key_name = self.__get_sort_index(
                db_sort_keys,
                query
            )


            if partition_filename:
                partition_data = self.db_manager.load_partition_data(db_name, partition_filename)
                if not partition_data: continue

                if sort_key_name and sort_key_name in partition_data:
                    partition_item = partition_data[sort_key_name]
                    is_valid = True

                    for attr_key, attr_value in query.items():
                        if attr_key not in partition_item: is_valid = False; break
                        if partition_item[attr_key] != attr_value: is_valid = False; break

                    if is_valid: 
                        del partition_data[sort_key_name]

                        if not partition_data:
                            self.db_manager.delete_partition(db_name, partition_name)

                        else:
                            self.db_manager.write_partition_data(db_name, partition_name, partition_data)


                elif not sort_key_name:

                    sort_keys_to_delete = []

                    for partition_item in partition_data.values():
                        is_valid = True

                        for attr_key, attr_value in query.items():
                            if attr_key not in partition_item: is_valid = False; break
                            if partition_item[attr_key] != attr_value: is_valid = False; break

                        if is_valid: 
                            sort_key_name = ""
                            for sort_key in db_sort_keys:
                                sort_key_name += f"{sort_key}={partition_item[sort_key]}"

                            sort_keys_to_delete.append(sort_key_name)


                    for sort_key_name in sort_keys_to_delete:
                        del partition_data[sort_key_name]
                    
                        if not partition_data:
                            self.db_manager.delete_partition(db_name, partition_name)

                        else:
                            self.db_manager.write_partition_data(db_name, partition_name, partition_data)


            else:
                for partition_name in self.db_manager.list_database_partitions(db_name):
                    partition_data = self.db_manager.load_partition_data(db_name, partition_name)
                    if not partition_data: continue

                    if sort_key_name and sort_key_name in partition_data:
                        partition_item = partition_data[sort_key_name]
                        is_valid = True

                        for attr_key, attr_value in query.items():
                            if attr_key not in partition_item: is_valid = False; break
                            if partition_item[attr_key] != attr_value: is_valid = False; break

                        if is_valid: 
                            del partition_data[sort_key_name]
                            if not partition_data:
                                self.db_manager.delete_partition(db_name, partition_name)

                            else:
                                self.db_manager.write_partition_data(db_name, partition_name, partition_data)


                    elif not sort_key_name:
                        sort_keys_to_delete = []

                        for partition_item in partition_data.values():
                            is_valid = True

                            for attr_key, attr_value in query.items():
                                if attr_key not in partition_item: is_valid = False; break
                                if partition_item[attr_key] != attr_value: is_valid = False; break

                            if is_valid: 
                                sort_key_name = ""
                                for sort_key in db_sort_keys:
                                    sort_key_name += f"{sort_key}={partition_item[sort_key]}"

                                sort_keys_to_delete.append(sort_key_name)


                        for sort_key_name in sort_keys_to_delete:
                            del partition_data[sort_key_name]
                        
                            if not partition_data:
                                self.db_manager.delete_partition(db_name, partition_name)

                            else:
                                self.db_manager.write_partition_data(db_name, partition_name, partition_data)

        return True        


    def __get_partition_filename(self, partition_keys, item):
        """Internal function to build partition filenames using a partition key sample and an item

        :param partition_keys list[str]: list of database partition key names
        :param item dict: Item used to build the filename
    
        :return str: partition name if the keys are found
        """

        partition_filename = ""

        for partition_key in partition_keys:
            
            if not partition_key in item:
                return ""
            
            partition_filename += f"{partition_key}={item[partition_key]}"

        return partition_filename
    

    def __get_sort_index(self, sort_keys, item):
        """Internal function to build sort key names using a sort key sample and an item

        :param sort_keys list[str]: list of database sort key names
        :param item dict: Item used to build the sort key
    
        :return str: sort key index if all the keys are found
        """
        
        sort_index = ""

        for sort_key in sort_keys:
            
            if not sort_key in item:
                return ""
            
            sort_index += f"{sort_key}={item[sort_key]}"

        return sort_index