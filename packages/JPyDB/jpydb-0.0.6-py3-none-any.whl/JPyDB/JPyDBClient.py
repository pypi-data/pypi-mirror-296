import os
from JPyDB.JPyDBManager import JPyDBManager


class JPyDBClient:

    def __init__(self): 
        self.db_manager = JPyDBManager()


    def get_items(self, table_name): 
        """Returns all table items

        :param table_name str: Name of the table

        :return list[dict]: List of table items
        """ 
        
        items = []

        for partition_name in self.db_manager.list_table_partitions(table_name):
            items = [*items, *self.db_manager.load_partition_data(table_name, partition_name).values()]

        return items
    

    def put_items(self, table_name, items):
        """Upserts items in the table

        :param table_name str: Name of the table
        :param items list|dict: List of items or item to insert
        
        :return bool: Flag indicating if the process was succeeded
        """

        partition_keys = self.db_manager.get_table_partition_keys(table_name)
        sort_keys = self.db_manager.get_table_sort_keys(table_name)

        if isinstance(items, dict):

            partition_filename = self.__get_partition_filename(partition_keys, items)
            if not partition_filename: return False

            sort_index = self.__get_sort_index(sort_keys, items)
            if not sort_index: return False

            partition_data = {sort_index: items}
            if self.db_manager.table_partition_exists(table_name, partition_filename):
                
                partition_data = self.db_manager.load_partition_data(table_name, partition_filename)
                partition_data[sort_index] = items

            self.db_manager.write_partition_data(table_name, partition_filename, partition_data)

        elif isinstance(items, list):

            for item in items:
                partition_filename = self.__get_partition_filename(partition_keys, item)
                if not partition_filename: return False

                sort_index = self.__get_sort_index(sort_keys, item)
                if not sort_index: return False
            
                partition_data = {sort_index: item}
                if self.db_manager.table_partition_exists(table_name, partition_filename):

                    partition_data = self.db_manager.load_partition_data(table_name, partition_filename)
                    partition_data[sort_index] = item

                self.db_manager.write_partition_data(table_name, partition_filename, partition_data)

        return True


    def query_items(self, table_name, query_list):
        """Search for similar items into a table

        :param table_name str: Name of the table
        :param query_list list[dict]: List of items to search 
        
        :return list: List of found items 
        """

        if not isinstance(query_list, list):
            return []
        
        for query in query_list:
            if not isinstance(query, dict):
                return []

        items = []

        db_partition_keys = self.db_manager.get_table_partition_keys(table_name)
        db_sort_keys = self.db_manager.get_table_sort_keys(table_name)

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
                partition_data = self.db_manager.load_partition_data(table_name, partition_filename)
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
                for partition_name in self.db_manager.list_table_partitions(table_name):
                    partition_data = self.db_manager.load_partition_data(table_name, partition_name)
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
    

    def delete_items(self, table_name, query_list):
        """Deletes similar items into a table 

        :param table_name str: Name of the table
        :param query_list list[dict]: List of items to delete

        :return bool: Flag indicating if the process was succeeded
        """

        if not isinstance(query_list, list):
            return False
        
        for query in query_list:
            if not isinstance(query, dict):
                return False

        sort_keys_to_delete = []

        db_partition_keys = self.db_manager.get_table_partition_keys(table_name)
        db_sort_keys = self.db_manager.get_table_sort_keys(table_name)

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
                partition_data = self.db_manager.load_partition_data(table_name, partition_filename)
                if not partition_data: 
                    self.db_manager.delete_partition(table_name, partition_filename)
                    continue

                if sort_key_name and sort_key_name in partition_data:
                    partition_item = partition_data[sort_key_name]
                    is_valid = True

                    for attr_key, attr_value in query.items():
                        if attr_key not in partition_item: is_valid = False; break
                        if partition_item[attr_key] != attr_value: is_valid = False; break

                    if is_valid: 
                        del partition_data[sort_key_name]

                        if not partition_data:
                            self.db_manager.delete_partition(table_name, partition_filename)

                        else:
                            self.db_manager.write_partition_data(table_name, partition_filename, partition_data)


                elif not sort_key_name:

                    sort_keys_to_delete = []

                    for partition_item in partition_data.values():
                        is_valid = True

                        for attr_key, attr_value in query.items():
                            if attr_key not in partition_item: is_valid = False; break
                            if partition_item[attr_key] != attr_value: is_valid = False; break

                        if is_valid: 
                            item_sort_key = self.__get_sort_index(db_sort_keys, partition_item)
                            sort_keys_to_delete.append(item_sort_key)


                    for item_sort_key in sort_keys_to_delete:
                        del partition_data[item_sort_key]
                    
                        if not partition_data:
                            self.db_manager.delete_partition(table_name, partition_filename)

                        else:
                            self.db_manager.write_partition_data(table_name, partition_filename, partition_data)


            else:
                for partition_filename in self.db_manager.list_table_partitions(table_name):
                
                    partition_data = self.db_manager.load_partition_data(table_name, partition_filename)

                    if not partition_data:
                        self.db_manager.delete_partition(table_name, partition_filename)
                        continue

                    if sort_key_name and sort_key_name in partition_data:
                        partition_item = partition_data[sort_key_name]
                        is_valid = True

                        for attr_key, attr_value in query.items():
                            if attr_key not in partition_item: is_valid = False; break
                            if partition_item[attr_key] != attr_value: is_valid = False; break

                        if is_valid: 
                            del partition_data[sort_key_name]
                            if not partition_data:
                                self.db_manager.delete_partition(table_name, partition_filename)

                            else:
                                self.db_manager.write_partition_data(table_name, partition_filename, partition_data)


                    elif not sort_key_name:
                        sort_keys_to_delete = []

                        for partition_item in partition_data.values():

                            is_valid = True

                            for attr_key, attr_value in query.items():
                                if attr_key not in partition_item: is_valid = False; break
                                if partition_item[attr_key] != attr_value: is_valid = False; break

                            if is_valid: 
                                item_sort_key = self.__get_sort_index(db_sort_keys, partition_item)
                                sort_keys_to_delete.append(item_sort_key)

                        for item_sort_key in sort_keys_to_delete:
                            del partition_data[item_sort_key]
                        
                            if not partition_data:
                                self.db_manager.delete_partition(table_name, partition_filename)

                            else:
                                self.db_manager.write_partition_data(table_name, partition_filename, partition_data)

        return True        


    def __get_partition_filename(self, partition_keys, item):
        """Internal function to build partition filenames using a partition key sample and an item

        :param partition_keys list[str]: list of table partition key names
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

        :param sort_keys list[str]: list of table sort key names
        :param item dict: Item used to build the sort key
    
        :return str: sort key index if all the keys are found
        """
        
        sort_index = ""

        for sort_key in sort_keys:
            
            if not sort_key in item:
                return ""
            
            sort_index += f"{sort_key}={item[sort_key]}"

        return sort_index