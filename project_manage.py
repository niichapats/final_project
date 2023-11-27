# import database module

import random

# import database module
import csv, os
from database import CSV, DB, Table

database = DB()
def initializing():

# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program
    read_csv = CSV()
    persons = read_csv.read('persons.csv')
    login = read_csv.read('login.csv')

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed
    persons_table = Table('persons', persons)
    login_table = Table('login', login)

    # add all these tables to the database
    database.insert(persons_table)
    database.insert(login_table)
    print(persons_table)
    print(login_table)




# define a funcion called login


def login():
    username = input('Enter username : ')
    password = input('Enter password: ')
    login_table = database.search('login')
    result = login_table.filter(lambda data: data['username'] == username and data['password'] == password)
    if len(result.table) != 0:
        return [result.table[0]['ID'], result.table[0]['role']]
    return None

# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None


# define a function called exit

def exit():
    writer = CSV()
    export_path = 'export/'
    writer.write(export_path + 'persons.csv', database.search('persons').select('*'))
    writer.write(export_path + 'login.csv', database.search('login').select('*'))
    writer.write(export_path + 'project.csv', database.search('project').select('*'))
    writer.write(export_path + 'advisor_pending_request.csv', database.search('advisor_pending_request').select('*'))
    writer.write(export_path + 'member_pending_request.csv', database.search('member_pending_request').select('*'))


# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

initializing()
val = login()
print(val)

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id


class Student:
    def __init__(self):
        self.role = 'student'
        self.num_request = 1
        self.name_request = ''

    def first_menu(self):
        print(f'1.see request : you have {self.num_request} request(s)')
        print(f'2.create project')
        ans = int(input('>> '))
        return ans

    def see_request(self):
        print(f'you have {self.num_request} from {self.name_request}')
        print('1.accept')
        print('2.dany')

    def deny_request(self):
        pass

    def accept_request(self):
        pass


    def to_lead(self):
        id_confirm = input('Enter your id to confirm project creation : ')
        if val[0] == id_confirm:
            self.role = 'lead'
            login_table = Table('login', database.search('login_table'))
            login_table.update('role', 'lead', id_confirm)
        else:
            print('Invalid id, can not crate a project.')

    # def create_project(self, lead):


# if val[1] = 'admin':
    # see and do admin related activities
# elif val[1] = 'student':
    # see and do student related activities
# elif val[1] = 'member':
    # see and do member related activities
# elif val[1] = 'lead':
    # see and do lead related activities
# elif val[1] = 'faculty':
    # see and do faculty related activities
# elif val[1] = 'advisor':
    # see and do advisor related activities


if val[1] == 'student':
    user = Student()
    ans1 = user.first_menu()
    print(ans1)
    if ans1 == 1:
        user.see_request()
    elif ans1 == 2:
        if user.num_request != 0:
            print('You must deny all member request first.')
            user.first_menu()
        else:
            user.to_lead()







# once everyhthing is done, make a call to the exit function
exit()
