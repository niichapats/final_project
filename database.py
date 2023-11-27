# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class CSV:
    def __init__(self):
        self.data = []

    def read(self, file_name):
        with open(os.path.join(__location__, file_name)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                self.data.append(dict(r))
        return self.data

# def read(file_name):
#     list_result = []
#     with open(os.path.join(__location__, file_name)) as f:
#         rows = csv.DictReader(f)
#         for r in rows:
#             list_result.append(dict(r))
#     return list_result


# add in code for a Database class

class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None

# add in code for a Table class


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
        self.list = []

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def insert(self, item):
        self.table.append(item)

    def update(self, key, value, dict_name):
        self.table.index(dict_name)[key] = value

    def __str__(self):
        return self.table_name + ':' + str(self.table)

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary

# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated
