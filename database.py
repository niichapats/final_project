# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class CSV:
    def __init__(self):
        self.data = []

    def read(self, file_name):
        self.data = []
        with open(os.path.join(__location__, file_name)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                self.data.append(dict(r))
        return self.data

    def write(self, file_name, data):
        if len(data) == 0:
            return False
        with open(os.path.join(__location__, file_name), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True

# def read_csv(file_name):
#     new_file = []
#     with open(os.path.join(__location__, file_name)) as f:
#         rows = csv.DictReader(f)
#         for r in rows:
#             new_file.append(dict(r))
#         return new_file


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

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    # def select(self, attributes_list):
    #     temps = []
    #     for item1 in self.table:
    #         dict_temp = {}
    #         for key in item1:
    #             if key in attributes_list:
    #                 dict_temp[key] = item1[key]
    #         temps.append(dict_temp)
    #     return temps

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if attributes_list == "*":
                    dict_temp[key] = item1[key]
                else:
                    if key in attributes_list:
                        dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def delete(self, condition):
        for row in self.table:
            if condition(row):
                self.table.remove(row)

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary
    def insert(self, item):
        self.table.append(item)

# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated
    def update(self, condition, key, value):
        new_table = self.filter(condition).table
        for row in new_table:
            row[key] = value

    def __str__(self):
        return self.table_name + ':' + str(self.table)
