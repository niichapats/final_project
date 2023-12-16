# import database module
from datetime import date
from random import randrange

from database import CSV, DB, Table
from session import Session

from model import person_table_model
from model import login_table_model
from model import project_table_model
from model import advisor_pending_request_table_model
from model import member_pending_request_table_model

database = DB()

def initializing():
    read_csv = CSV()
    person_file = read_csv.read('export/persons.csv')
    login_file = read_csv.read('export/login.csv')
    project_file = read_csv.read('export/project.csv')
    member_file = read_csv.read('export/member_pending_request.csv')
    advisor_file = read_csv.read('export/advisor_pending_request.csv')

    person_table = Table('person_table', person_file)
    login_table = Table('login_table', login_file)
    project_table = Table('project_table', project_file)
    advisor_pending_request_table = Table('advisor_pending_request', advisor_file)
    member_pending_request_table = Table('member_pending_request', member_file)

    database.insert(person_table)
    database.insert(login_table)
    database.insert(project_table)
    database.insert(advisor_pending_request_table)
    database.insert(member_pending_request_table)


def login():
    username = input('Enter username : ')
    password = input('Enter password : ')
    login_table = database.search('login_table')
    this_data = login_table.filter(lambda x: x['username'] == username and x['password'] == password)
    this_data = this_data.table
    if len(this_data) == 0:
        print('Invalid username or password')
        return None
    return [this_data[0]['ID'], this_data[0]['role']]


# class Project:
#     def __init__(self, project_id, lead, title):
#         self.project_id = project_id
#         self.lead = lead
#         self.title = title
#         self.member1 = None
#         self.member2 = None
#         self.advisor = None
#         self.status = 'Processing'
#         self.evaluator1 = None
#         self.evaluator2 = None
#         self.num_member = 0
#         self.num_advisor = 0
#         self.num_approve = 0



########################################################################################

class Student:
    global database

    def __init__(self, std_id):
        self.std_id = std_id
        self.request = 0

    @staticmethod
    def menu():
        print()
        print('Student Menu')
        print('1. Check request(s)')
        print('2. Create project')
        print('0. Logout')

    def create_project(self, title):
        while True:
            project_id = f'{randrange(1, 1000):04}'
            check_id = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id)
            if len(check_id.table) == 0:
                new_project = project_table_model.copy()
                new_project['ProjectID'] = project_id
                new_project['Lead'] = self.std_id
                new_project['Title'] = title
                new_project['Status'] = 'processing'
                database.search('project_table').insert(new_project)
                print('Create project successfully.')
                break

    def first_count_request(self):
        request = database.search('member_pending_request').filter(lambda x: x['to_be_member'] == self.std_id).table
        for row in request:
            if row['to_be_member'] == self.std_id:
                self.request += 1

    def check_request(self):
        request = database.search('member_pending_request').filter(lambda x: x['to_be_member'] == self.std_id).table
        if self.request == 0:
            print('There is no request(s)')
        else:
            for row in request:
                if row['to_be_member'] == self.std_id:
                    project_id = row['ProjectID']
                    project = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id).table
                    print(f'You have {self.request} request(s)')
                    print(f'Project id : {row["ProjectID"]}')
                    print(f'Title : {project[0]["Title"]}')
                    print(f'Leader : {project[0]["Lead"]}')
                    print()
            print('1. Accept request')
            print('2. Deny request')
            acc_de = int(input(': '))
            if acc_de == 1:
                project_id = input('Enter the project id that you want tp accept : ')
                self.accept_request(project_id)
            elif acc_de == 2:
                project_id = input('Enter the project id that you want tp deny : ')
                self.deny_request(project_id)
            else:
                print('Invalid command')

    def accept_request(self, project_id):
        database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response', 'Accept')
        today = date.today()
        today_format = today.strftime('%d/%m/%Y')
        database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date', today_format)
        self.request = 0
        database.search('login_table').update(lambda x: x['ID'] == self.std_id, 'role', 'member')
        database.search('person_table').update(lambda x: x['ID'] == self.std_id, 'type', 'member')
        data_table = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id).table
        if data_table[0]['Member1'] == '':
            database.search('project_table').update(lambda x: x['ProjectID'] == project_id, 'Member1', self.std_id)
        else:
            database.search('project_table').update(lambda x: x['ProjectID'] == project_id, 'Member2', self.std_id)

    def deny_request(self, project_id):
        database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response', 'Deny')
        today = date.today()
        today_format = today.strftime('%d/%m/%Y')
        database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date', today_format)
        self.request -= 1

    def deny_all_request(self):
        all_request = database.search('member_pending_request').filter(lambda x: x['to_be_member'] == self.std_id).table
        for i in range(len(all_request)):
            project_id = all_request[0]['ProjectID']
            database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response', 'Deny')
            today = date.today()
            today_format = today.strftime('%d/%m/%Y')
            database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date', today_format)
        self.request = 0

    def role_to_lead(self):
        database.search('login_table').update(lambda x: x['ID'] == self.std_id, 'role', 'lead')
        database.search('person_table').update(lambda x: x['ID'] == self.std_id, 'type', 'lead')
        print("Your role has changed to lead student. Please logout and login again.")

    def run_menu(self):
        self.first_count_request()
        while True:
            self.menu()
            std_command = int(input(': '))
            if std_command == 1:  #check request then choose to accept or deny
                self.check_request()

            elif std_command == 2:  #create project
                while True:
                    if self.request != 0:
                        print('You must deny all member requests before creating the project.')
                        print('1. Deny all member requests and create project')
                        print('2. Cancel project creation')
                        std_command = int(input('Enter number : '))
                        if std_command == 1:
                            self.deny_all_request()
                            print('Denied all member requests')
                            title = input('Enter your project title : ')
                            self.create_project(title)
                            self.role_to_lead()
                        elif std_command == 2:
                            break
                    else:
                        title = input('Enter your project title : ')
                        self.create_project(title)
                        self.role_to_lead()
                        break
            elif std_command == 0:
                print('logout successfully')
                print()
                break

    def set_request(self, request):
        self.request = request


########################################################################################


class Lead:
    global database

    def __init__(self, std_id):
        self.std_id = std_id

    def menu(self):
        print()
        print('Lead menu')
        print('1. Send request member')
        print('2. Check pending member status')
        print('3. Send request advisor')
        print('4. Check pending advisor status')
        print('5. Send proposal')
        print('6. Send project')
        print('7. Check project status')
        print('8. Check project details')
        print('9. Delete project')
        print('0. Logout')

    def send_request(self):
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id).table
        num_member = 0
        print(project)
        for row in project:
            print(row['Member1'])
            print(row['Member2'])
            if row['Member1'] != '':
                num_member += 1
            if row['Member2'] != '':
                num_member += 1

        if num_member == 2:
            print('You already have 2 members. Cannot request more member.')
        else:
            print(f'You have {num_member} member(s). You can request {2 - num_member} more.')
            mem_id = input('Enter member ID : ')
            check_type = database.search('person_table').filter(lambda x: x['ID'] == mem_id).table
            print(check_type)
            if check_type[0]['type'] == 'student':
                project_id = project[0]['ProjectID']
                member_row = member_pending_request_table_model.copy()
                member_row['ProjectID'] = project_id
                member_row['to_be_member'] = mem_id
                member_row['Response'] = ''
                member_row['Response_date'] = ''
                database.search('member_pending_request').insert(member_row)
                print(database.search('member_pending_request'))
            else:
                print('Cannot request him/her.')

    def pending_member_status(self):
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_tb = project.table
        project_id = project_tb[0]['ProjectID']
        member_pending_request = database.search('member_pending_request').filter(lambda x: x['ProjectID'] == project_id)
        member_tb = member_pending_request.table
        for row in member_tb:
            std_id = row["to_be_member"]
            mem_data = database.search('person_table').filter(lambda x: x['ID'] == std_id)
            mem_data = mem_data.table
            first = mem_data[0]['fist']
            last = mem_data[0]['last']
            print(f'Name : {first} {last}    Response : {row["Response"]}')

    def run_menu(self):
        while True:
            self.menu()
            lead_command = int(input(': '))
            if lead_command == 1:
                self.send_request()
            elif lead_command == 2:
                self.pending_member_status()
            elif lead_command == 0:
                print('logout successfully')
                print()
                break



# define a function called exit

def exit():
    writer = CSV()
    export_path = 'export/'
    writer.write(export_path + 'persons.csv', database.search('person_table').select('*'))
    writer.write(export_path + 'login.csv', database.search('login_table').select('*'))
    writer.write(export_path + 'project.csv', database.search('project_table').select('*'))
    writer.write(export_path + 'advisor_pending_request.csv', database.search('advisor_pending_request').select('*'))
    writer.write(export_path + 'member_pending_request.csv', database.search('member_pending_request').select('*'))


# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:

   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python






########################################################################################


# make calls to the initializing and login functions defined above

initializing()
# person_table = database.search('person_table')
# login_table = database.search('login_table')
# project_table = database.search('project_table')
# member_pending_request = database.search('member_pending_request')
# advisor_pending_request = database.search('advisor_pending_request')

while True:
    command = input('Enter the command (login / exit) : ')
    if command == 'exit':
        print('Exiting the program...')
        exit()
        break
    elif command == 'login':
        val = login()
        if val[1] == 'admin':
            print('admin')
            pass
        elif val[1] == 'student':
            student = Student(val[0])
            student.run_menu()
        elif val[1] == 'member':
            print('member')
            pass
        elif val[1] == 'lead':
            lead = Lead(val[0])
            lead.run_menu()
        elif val[1] == 'faculty':
            print('faculty')
            pass
        elif val[1] == 'advisor':
            print('advisor')
            pass

#################################################


# once everyhthing is done, make a call to the exit function
# exit()
