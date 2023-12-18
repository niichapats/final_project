# import database module
from datetime import date
from random import randrange

from database import CSV, DB, Table

from model import person_table_model
from model import login_table_model
from model import project_table_model
from model import advisor_pending_request_table_model
from model import member_pending_request_table_model
from model import proposal_project_table_model
from model import evaluate_project_table_model

database = DB()


def initializing():
    read_csv = CSV()
    person_file = read_csv.read('data/persons.csv')
    login_file = read_csv.read('data/login.csv')
    project_file = read_csv.read('data/project.csv')
    member_file = read_csv.read('data/member_pending_request.csv')
    advisor_file = read_csv.read('data/advisor_pending_request.csv')
    proposal_project_file = read_csv.read('data/proposal_project.csv')
    evaluate_file = read_csv.read('data/evaluate.csv')

    person_table = Table('person_table', person_file)
    login_table = Table('login_table', login_file)
    project_table = Table('project_table', project_file)
    member_pending_request_table = Table('member_pending_request', member_file)
    advisor_pending_request_table = Table('advisor_pending_request', advisor_file)
    proposal_project_table = Table('proposal_project', proposal_project_file)
    evaluate_table = Table('evaluate', evaluate_file)

    database.insert(person_table)
    database.insert(login_table)
    database.insert(project_table)
    database.insert(advisor_pending_request_table)
    database.insert(member_pending_request_table)
    database.insert(proposal_project_table)
    database.insert(evaluate_table)


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

    @staticmethod
    def get_name(role, the_id):
        project = database.search('project_table').filter(lambda x: x[role] == the_id)
        project_tb = project.table
        role_id = project_tb[0][role]
        if role_id == '':
            return '-'
        else:
            person = database.search('person_table').filter(lambda x: x['ID'] == role_id)
            joined_data = project.join(person, role, 'ID')
            joined_table = joined_data.table
            role_name = joined_table[0]['fist']
            role_last = joined_table[0]['last']
            return f'{role_name} {role_last}'

    def create_project(self, title):
        # Check if you already have a project or not
        check_project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        check_project_tb = check_project.table
        if not check_project_tb:
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
        else:
            print('Cannot create the project. You already have one.')

    def first_count_request(self):
        request = database.search('member_pending_request').filter(lambda x: x['to_be_member'] == self.std_id).table
        for row in request:
            if row['to_be_member'] == self.std_id:
                self.request += 1

    def check_request(self):
        # check if there is a request to be a member sent to you or not, then choose to accept or deny
        request = database.search('member_pending_request').filter(lambda x: x['to_be_member'] == self.std_id).table
        if self.request == 0:
            print('There is no request(s)')
        else:
            for row in request:
                if row['to_be_member'] == self.std_id:
                    project_id = row['ProjectID']
                    project = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id).table
                    lead_id = project[0]["Lead"]
                    lead_name = self.get_name('Lead', lead_id)
                    print(f'You have {self.request} request(s)')
                    print(f'Project id : {row["ProjectID"]}')
                    print(f'Title : {project[0]["Title"]}')
                    print(f'Leader : {lead_name}')
                    print()
            print('1. Accept request')
            print('2. Deny request')
            print('3. back to Student Menu')
            acc_de = int(input(': '))
            if acc_de == 1:
                project_id = input('Enter the project id that you want to accept : ')
                self.accept_request(project_id)
                print('Accepted request successfully.')
            elif acc_de == 2:
                project_id = input('Enter the project id that you want to deny : ')
                self.deny_request(project_id)
                print('Denied request successfully.')
            elif acc_de == 3:
                pass
            else:
                print('Invalid command')
        input('[ Press "enter" to go back to the menu ]')

    def accept_request(self, project_id):
        database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response', 'Accept')
        today = date.today()
        today_format = today.strftime('%d/%m/%Y')
        database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date',
                                                         today_format)
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
        database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date',
                                                         today_format)
        self.request -= 1

    def deny_all_request(self):
        all_request = database.search('member_pending_request').filter(lambda x: x['to_be_member'] == self.std_id).table
        for i in range(len(all_request)):
            project_id = all_request[0]['ProjectID']
            database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response', 'Deny')
            today = date.today()
            today_format = today.strftime('%d/%m/%Y')
            database.search('member_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date',
                                                             today_format)
        self.request = 0

    def role_to_lead(self):
        database.search('login_table').update(lambda x: x['ID'] == self.std_id, 'role', 'lead')
        database.search('person_table').update(lambda x: x['ID'] == self.std_id, 'type', 'lead')
        print("Your role has changed to lead student. Please logout and login again.")
        input('[ Press "enter" to go back to the menu ]')

    def run_menu(self):
        self.first_count_request()
        while True:
            self.menu()
            std_command = int(input(': '))
            if std_command == 1:  # check request then choose to accept or deny
                self.check_request()

            elif std_command == 2:  # create project
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
            else:
                print('Invalid command')

    def set_request(self, request):
        self.request = request


class Lead:
    global database

    def __init__(self, std_id):
        self.std_id = std_id

    def get_project_id(self):
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_tb = project.table
        project_id = project_tb[0]['ProjectID']
        return project_id

    def get_name(self, role):
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_tb = project.table
        role_id = project_tb[0][role]
        if role_id == '':
            return '-'
        else:
            person = database.search('person_table').filter(lambda x: x['ID'] == role_id)
            joined_data = project.join(person, role, 'ID')
            joined_table = joined_data.table
            role_name = joined_table[0]['fist']
            role_last = joined_table[0]['last']
            return f'{role_name} {role_last}'

    def get_role_id(self, role):
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_tb = project.table
        role_id = project_tb[0][role]
        return role_id

    @staticmethod
    def menu():
        print()
        print('Lead Menu')
        print('1. Send request member')
        print('2. Check pending member status')
        print('3. Request advisor')
        print('4. Check pending advisor status')
        print('5. Send proposal')
        print('6. Send project(evaluate)')
        print('7. Check project status')
        print('8. Check project details')
        print('0. Logout')

    def send_request(self):
        # send request to other students to be a member
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id).table
        num_member = 0
        # count the number of members
        for row in project:
            if row['Member1'] != '':
                num_member += 1
            if row['Member2'] != '':
                num_member += 1

        if num_member == 2:
            print('You already have 2 members. Cannot request more member.')
        else:
            print(f'You have {num_member} member(s). You can request {2 - num_member} more.')
            mem_id = input('Enter member ID : ')
            check_type_data = database.search('person_table').filter(lambda x: x['ID'] == mem_id)
            check_type = check_type_data.table
            if not check_type:
                print('Not Found this ID')
            elif check_type[0]['type'] == 'student':  # Check that the role is student. You can send a request to student only
                project_id = project[0]['ProjectID']
                member_row = member_pending_request_table_model.copy()
                member_row['ProjectID'] = project_id
                member_row['to_be_member'] = mem_id
                member_row['Response'] = ''
                member_row['Response_date'] = ''
                database.search('member_pending_request').insert(member_row)
                print('Sent request successfully.')
            else:
                print('Cannot request him/her.')
        input('[ Press "enter" to go back to the menu ]')

    def pending_member_status(self):
        project_id = self.get_project_id()
        member_pending_request = database.search('member_pending_request').filter(
            lambda x: x['ProjectID'] == project_id)
        member_tb = member_pending_request.table
        if not member_tb:
            print("You haven't sent any request yet.")
        else:
            for row in member_tb:
                std_id = row["to_be_member"]
                mem_data = database.search('person_table').filter(lambda x: x['ID'] == std_id)
                mem_data = mem_data.table
                first = mem_data[0]['fist']
                last = mem_data[0]['last']
                if row["Response"] == '':
                    response = "Haven't responded yet."
                else:
                    response = row["Response"]
                print(f'Name : {first} {last}    Response : {response}')
        print()
        input('[ Press "enter" to go back to the menu ]')

    def request_advisor(self):
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_tb = project.table
        check_adv = project_tb[0]['Advisor']
        if check_adv != '':
            print('Cannot request. You already have the advisor for this project.')
        else:
            name_adv = input('Enter the advisor name : ')
            last_adv = input('Enter the advisor lastname : ')
            adv_data = database.search('person_table').filter(lambda x: x['fist'] == name_adv and x['last'] == last_adv)
            adv_tb = adv_data.table
            check_role = adv_tb[0]['type']
            adv_id = adv_tb[0]['ID']
            project_id = self.get_project_id()
            if check_role != 'faculty':  # Check that the role is student. You can send a request to student only
                print('Cannot request. He/She is not a faculty.')
            else:
                new_request = advisor_pending_request_table_model.copy()
                new_request['ProjectID'] = project_id
                new_request['to_be_advisor'] = adv_id
                database.search('advisor_pending_request').insert(new_request)
                print('Sent request successfully.')
        input('[ Press "enter" to go back to the menu ]')

    def pending_advisor_status(self):
        project_id = self.get_project_id()
        advisor_pending_request = database.search('advisor_pending_request').filter(
            lambda x: x['ProjectID'] == project_id)
        advisor_tb = advisor_pending_request.table
        if not advisor_tb:
            print("You haven't sent any request yet.")
        else:
            for row in advisor_tb:
                fac_id = row["to_be_advisor"]
                adv_data = database.search('person_table').filter(lambda x: x['ID'] == fac_id)
                adv_data = adv_data.table
                first = adv_data[0]['fist']
                last = adv_data[0]['last']
                if row["Response"] == '':
                    response = "Haven't responded yet."
                else:
                    response = row["Response"]
                print(f'Name : {first} {last}    Response : {response}')
        print()
        input('[ Press "enter" to go back to the menu ]')

    def send_proposal(self):
        project_data = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_table = project_data.table
        proposal_data = database.search('proposal_project').filter(lambda x: x['Lead'] == self.std_id)
        proposal_table = proposal_data.table
        if project_table[0]['Advisor'] == '':
            print('Cannot send the proposal. Please request advisor and wait for him/her to accept first. ')
        elif proposal_table[0]['Status'] == 'Rejected':
            print('Your recent proposal has been rejected. You can send it again.')
            proposal = input('Enter your proposal: ')
            database.search('proposal_project').update(lambda x: x['Lead'] == self.std_id, 'Proposal', proposal)
        else:
            proposal = input('Enter your proposal: ')
            project_id = self.get_project_id()
            new_proposal = proposal_project_table_model.copy()
            advisor_id = self.get_role_id('Advisor')
            new_proposal['ProjectID'] = project_id
            new_proposal['Lead'] = self.std_id
            new_proposal['Advisor'] = advisor_id
            new_proposal['Proposal'] = proposal
            new_proposal['Status'] = 'Waiting'
            database.search('proposal_project').insert(new_proposal)
            print(f'Sent proposal to the advisor({self.get_name("Advisor")}) successfully.')
        input('[ Press "enter" to go back to the menu ]')

    def send_project(self):
        project = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_tb = project.table
        project_title = project_tb[0]['Title']
        project_id = self.get_project_id()
        advisor_id = self.get_role_id('Advisor')
        project = f'{project_title}(file)'

        # for check proposal and check if the project has been submitted or not
        proposal_project = database.search('proposal_project').filter(lambda x: x['Lead'] == self.std_id)
        proposal_project_tb = proposal_project.table
        evaluate = database.search('evaluate').filter(lambda x: x['Lead'] == self.std_id)
        evaluate_tb = evaluate.table

        # random evaluator
        faculty_data = database.search('person_table').filter(lambda x: x['type'] == 'faculty')
        faculty_table = faculty_data.table
        num_fac = len(faculty_table)
        random_num = randrange(0, num_fac)
        evaluator_id = faculty_table[random_num]['ID']
        evaluator_name = faculty_table[random_num]['fist']
        evaluator_last = faculty_table[random_num]['last']

        if not proposal_project_tb:
            print('Cannot send the project. Please send the proposal first.')
        elif proposal_project_tb[0]['Status'] == 'Waiting':
            print('Please wait for the advisor to approve the proposal first.')
        elif evaluate_tb:
            evaluate_status = evaluate_tb[0]['Status']
            if evaluate_status == 'Waiting':
                print('You have already submitted the project. Please wait for the evaluator to approve the project.')
        else:
            new_evaluate = evaluate_project_table_model.copy()
            new_evaluate['ProjectID'] = project_id
            new_evaluate['Lead'] = self.std_id
            new_evaluate['Advisor'] = advisor_id
            new_evaluate['Project'] = project
            new_evaluate['Evaluator'] = evaluator_id
            new_evaluate['Status'] = 'Waiting'
            database.search('evaluate').insert(new_evaluate)
            print(f'Sent project to the evaluator({evaluator_name} {evaluator_last}) successfully.')
        input('[ Press "enter" to go back to the menu ]')

    def check_status(self):
        proposal_project = database.search('proposal_project').filter(lambda x: x['Lead'] == self.std_id)
        evaluate_project = database.search('evaluate').filter(lambda x: x['Lead'] == self.std_id)
        proposal_project_tb = proposal_project.table
        evaluate_project_tb = evaluate_project.table
        if not proposal_project_tb:
            proposal_status = "Haven't submit yet."
        else:
            proposal_status = proposal_project_tb[0]['Status']
        if not evaluate_project_tb:
            project_status = "Haven't submit yet."
        else:
            project_status = evaluate_project_tb[0]['Status']
        print(f'Proposal status : {proposal_status}')
        print(f'Project status : {project_status}')
        print()
        input('[ Press "enter" to go back to the menu ]')

    def check_details(self):
        project_data = database.search('project_table').filter(lambda x: x['Lead'] == self.std_id)
        project_table = project_data.table
        lead_name = self.get_name('Lead')
        mem1_name = self.get_name('Member1')
        mem2_name = self.get_name('Member2')
        advisor_name = self.get_name('Advisor')
        print('( Project details )')
        print(f"Project ID : {project_table[0]['ProjectID']}")
        print(f"Title : {project_table[0]['Title']}")
        print(f"Leader : {lead_name}")
        print(f"Member1 : {mem1_name}")
        print(f"Member2 : {mem2_name}")
        print(f"Advisor : {advisor_name}")
        print(f"Status : {project_table[0]['Status']}")
        input('[ Press "enter" to go back to the menu ]')

    def run_menu(self):
        while True:
            self.menu()
            lead_command = int(input(': '))
            if lead_command == 1:
                self.send_request()
            elif lead_command == 2:
                self.pending_member_status()
            elif lead_command == 3:
                self.request_advisor()
            elif lead_command == 4:
                self.pending_advisor_status()
            elif lead_command == 5:
                self.send_proposal()
            elif lead_command == 6:
                self.send_project()
            elif lead_command == 7:
                self.check_status()
            elif lead_command == 8:
                self.check_details()
            elif lead_command == 0:
                print('logout successfully')
                print()
                break
            else:
                print('Invalid command')


class Member:
    global database

    def __init__(self, std_id):
        self.std_id = std_id
        self.role = ''

    def check_mem_role(self):
        # check that you are member1 or member2
        mem1 = database.search('project_table').filter(lambda x: x['Member1'] == self.std_id)
        mem1_tb = mem1.table
        if not mem1_tb:
            return 'Member2'
        else:
            return 'Member1'

    def set_role(self, role):
        self.role = role

    def get_project_id(self):
        project = database.search('project_table').filter(lambda x: x[self.role] == self.std_id)
        project_tb = project.table
        project_id = project_tb[0]['ProjectID']
        return project_id

    def get_name(self, role):
        project = database.search('project_table').filter(lambda x: x[self.role] == self.std_id)
        project_tb = project.table
        role_id = project_tb[0][role]
        if role_id == '':
            return '-'
        else:
            person = database.search('person_table').filter(lambda x: x['ID'] == role_id)
            joined_data = project.join(person, role, 'ID')
            joined_table = joined_data.table
            role_name = joined_table[0]['fist']
            role_last = joined_table[0]['last']
            return f'{role_name} {role_last}'

    @staticmethod
    def menu():
        print()
        print('Member Menu')
        print('1. Check pending member status')
        print('2. Check pending advisor status')
        print('3. Check project status')
        print('4. Check project details')
        print('0. Logout')

    def pending_member_status(self):
        project_id = self.get_project_id()
        member_pending_request = database.search('member_pending_request').filter(
            lambda x: x['ProjectID'] == project_id)
        member_tb = member_pending_request.table
        if not member_tb:
            print("Your leader haven't sent any request yet.")
        else:
            for row in member_tb:
                std_id = row["to_be_member"]
                mem_data = database.search('person_table').filter(lambda x: x['ID'] == std_id)
                mem_data = mem_data.table
                first = mem_data[0]['fist']
                last = mem_data[0]['last']
                if row["Response"] == '':
                    response = "Haven't responded yet."
                else:
                    response = row["Response"]
                print(f'Name : {first} {last}    Response : {response}')
        print()
        input('[ Press "enter" to go back to the menu ]')

    def pending_advisor_status(self):
        project_id = self.get_project_id()
        advisor_pending_request = database.search('advisor_pending_request').filter(
            lambda x: x['ProjectID'] == project_id)
        advisor_tb = advisor_pending_request.table
        if not advisor_tb:
            print("You haven't sent any request yet.")
        else:
            for row in advisor_tb:
                fac_id = row["to_be_advisor"]
                adv_data = database.search('person_table').filter(lambda x: x['ID'] == fac_id)
                adv_data = adv_data.table
                first = adv_data[0]['fist']
                last = adv_data[0]['last']
                if row["Response"] == '':
                    response = "Haven't responded yet."
                else:
                    response = row["Response"]
                print(f'Name : {first} {last}    Response : {response}')
        print()
        input('[ Press "enter" to go back to the menu ]')

    def check_status(self):
        project_id = self.get_project_id()
        proposal_project = database.search('proposal_project').filter(lambda x: x['ProjectID'] == project_id)
        evaluate_project = database.search('evaluate').filter(lambda x: x['ProjectID'] == project_id)
        proposal_project_tb = proposal_project.table
        evaluate_project_tb = evaluate_project.table
        if not proposal_project_tb:
            proposal_status = "Haven't submit yet."
        else:
            proposal_status = proposal_project_tb[0]['Status']
        if not evaluate_project_tb:
            project_status = "Haven't submit yet."
        else:
            project_status = evaluate_project_tb[0]['Status']
        print(f'Proposal status : {proposal_status}')
        print(f'Project status : {project_status}')
        print()
        input('[ Press "enter" to go back to the menu ]')

    def check_details(self):
        project_data = database.search('project_table').filter(lambda x: x[self.role] == self.std_id)
        project_table = project_data.table
        lead_name = self.get_name('Lead')
        mem1_name = self.get_name('Member1')
        mem2_name = self.get_name('Member2')
        advisor_name = self.get_name('Advisor')
        print('( Project details )')
        print(f"Project ID : {project_table[0]['ProjectID']}")
        print(f"Title : {project_table[0]['Title']}")
        print(f"Leader : {lead_name}")
        print(f"Member1 : {mem1_name}")
        print(f"Member2 : {mem2_name}")
        print(f"Advisor : {advisor_name}")
        print(f"Status : {project_table[0]['Status']}")
        input('[ Press "enter" to go back to the menu ]')

    def run_menu(self):
        role = self.check_mem_role()
        self.role = role
        while True:
            self.menu()
            lead_command = int(input(': '))
            if lead_command == 1:
                self.pending_member_status()
            elif lead_command == 2:
                self.pending_advisor_status()
            elif lead_command == 3:
                self.check_status()
            elif lead_command == 4:
                self.check_details()
            elif lead_command == 0:
                print('logout successfully')
                print()
                break
            else:
                print('Invalid command')


class Faculty:
    global database

    def __init__(self, fac_id):
        self.fac_id = fac_id
        self.request = 0

    @staticmethod
    def menu():
        print()
        print('Faculty Menu')
        print('1. Check request to be an advisor')
        print('2. Evaluate project')
        print('0. Logout')

    @staticmethod
    def get_name(role, the_id):
        project = database.search('project_table').filter(lambda x: x[role] == the_id)
        project_tb = project.table
        role_id = project_tb[0][role]
        if role_id == '':
            return '-'
        else:
            person = database.search('person_table').filter(lambda x: x['ID'] == role_id)
            joined_data = project.join(person, role, 'ID')
            joined_table = joined_data.table
            role_name = joined_table[0]['fist']
            role_last = joined_table[0]['last']
            return f'{role_name} {role_last}'

    def first_count_request(self):
        request = database.search('advisor_pending_request').filter(lambda x: x['to_be_advisor'] == self.fac_id).table
        for row in request:
            if row['to_be_advisor'] == self.fac_id:
                self.request += 1

    def check_request(self):
        # check if there is a request to be an advisor sent to you or not, then choose to accept or deny
        request = database.search('advisor_pending_request').filter(lambda x: x['to_be_advisor'] == self.fac_id).table
        if self.request == 0:
            print('There is no request(s)')
        else:
            for row in request:
                if row['to_be_advisor'] == self.fac_id:
                    project_id = row['ProjectID']
                    project = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id).table
                    lead_id = project[0]["Lead"]
                    lead_name = self.get_name('Lead', lead_id)
                    print(f'You have {self.request} request(s)')
                    print(f'Project id : {row["ProjectID"]}')
                    print(f'Title : {project[0]["Title"]}')
                    print(f'Leader : {lead_name}')
                    print()
            print('1. Accept request')
            print('2. Deny request')
            print('3. back to Faculty Menu')
            eva = int(input(': '))
            if eva == 1:
                project_id = input('Enter the project id that you want tp accept : ')
                self.accept_request_adv(project_id)
                print('Accepted request successfully.')
            elif eva == 2:
                project_id = input('Enter the project id that you want tp deny : ')
                self.deny_request(project_id)
                print('Denied request successfully.')
            elif eva == 3:
                pass
            else:
                print('Invalid command')
        input('[ Press "enter" to go back to the menu ]')

    def accept_request_adv(self, project_id):
        database.search('advisor_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response', 'Accept')
        today = date.today()
        today_format = today.strftime('%d/%m/%Y')
        database.search('advisor_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date',
                                                          today_format)
        self.request = 0
        database.search('login_table').update(lambda x: x['ID'] == self.fac_id, 'role', 'advisor')
        database.search('person_table').update(lambda x: x['ID'] == self.fac_id, 'type', 'advisor')
        database.search('project_table').update(lambda x: x['ProjectID'] == project_id, 'Advisor', self.fac_id)

    def deny_request(self, project_id):
        database.search('advisor_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response', 'Deny')
        today = date.today()
        today_format = today.strftime('%d/%m/%Y')
        database.search('advisor_pending_request').update(lambda x: x['ProjectID'] == project_id, 'Response_date',
                                                          today_format)
        self.request -= 1

    def evaluate(self):
        evaluate_data = database.search('evaluate').filter(lambda x: x['Evaluator'] == self.fac_id)
        evaluate_table = evaluate_data.table
        if not evaluate_table:
            print('There are not projects to evaluate.')
        else:
            for row in evaluate_table:
                lead_id = row['Lead']
                advisor_id = row['Advisor']
                print(f'Project ID : {row["ProjectID"]}')
                print(f'Leader : {self.get_name("Lead", lead_id)}')
                print(f'Advisor : {self.get_name("Advisor", advisor_id)}')
                print(f'Project : {row["Project"]}')
                print()
                print('1. Approve project')
                print('2. Dany Project')
                print('3. Back to Faculty Menu')
                fac_command = int(input(': '))
                if fac_command == 1:
                    project_id = input('Enter the project id that you want to approve : ')
                    database.search('evaluate').update(lambda x: x['ProjectID'] == project_id, 'Evaluator', self.fac_id)
                    database.search('evaluate').update(lambda x: x['ProjectID'] == project_id, 'Status', 'Approved')
                    database.search('project_table').update(lambda x: x['ProjectID'] == project_id, 'Status', 'Approved')
                    print('Approved project successfully.')
                elif fac_command == 2:
                    project_id = input('Enter the project id that you want to reject : ')
                    database.search('evaluate').update(lambda x: x['ProjectID'] == project_id, 'Evaluator', self.fac_id)
                    database.search('evaluate').update(lambda x: x['ProjectID'] == project_id, 'Status', 'Rejected')
                    database.search('project_table').update(lambda x: x['ProjectID'] == project_id, 'Status',
                                                            'Rejected')
                    print('Rejected project successfully.')
                elif fac_command == 3:
                    pass
                else:
                    print('Invalid command')
        input('[ Press "enter" to go back to the menu ]')

    def set_request(self, request):
        self.request = request

    def run_menu(self):
        self.first_count_request()
        while True:
            self.menu()
            lead_command = int(input(': '))
            if lead_command == 1:
                self.check_request()
            elif lead_command == 2:
                self.evaluate()
            elif lead_command == 0:
                print('logout successfully')
                print()
                break
            else:
                print('Invalid command')


class Advisor:
    global database

    def __init__(self, adv_id):
        self.adv_id = adv_id

    @staticmethod
    def menu():
        print()
        print('Advisor Menu')
        print('1. See my project details')
        print('2. Check proposal')
        print('   (show the details about the project I am advising on)')
        print('0. Logout')

    def get_name(self, role):
        project = database.search('project_table').filter(lambda x: x['Advisor'] == self.adv_id)
        project_tb = project.table
        role_id = project_tb[0][role]
        if role_id == '':
            return '-'
        else:
            person = database.search('person_table').filter(lambda x: x['ID'] == role_id)
            joined_data = project.join(person, role, 'ID')
            joined_table = joined_data.table
            role_name = joined_table[0]['fist']
            role_last = joined_table[0]['last']
            return f'{role_name} {role_last}'

    def check_details(self):
        project_data = database.search('project_table').filter(lambda x: x['Advisor'] == self.adv_id)
        project_table = project_data.table
        lead_name = self.get_name('Lead')
        mem1_name = self.get_name('Member1')
        mem2_name = self.get_name('Member2')
        advisor_name = self.get_name('Advisor')
        print('( Project details )')
        print(f"Project ID : {project_table[0]['ProjectID']}")
        print(f"Title : {project_table[0]['Title']}")
        print(f"Leader : {lead_name}")
        print(f"Member1 : {mem1_name}")
        print(f"Member2 : {mem2_name}")
        print(f"Advisor : {advisor_name}")
        print(f"Status : {project_table[0]['Status']}")
        input('[ Press "enter" to go back to the menu ]')

    def check_proposal(self):
        # check if there is a proposal sent to you or not, then choose to accept or reject
        proposal = database.search('proposal_project').filter(lambda x: x['Advisor'] == self.adv_id)
        proposal_tb = proposal.table
        if not proposal:
            print('No proposal approval request.')
        else:
            print('Proposal')
            print(f'{proposal_tb[0]["Proposal"]}')
            print()
            print('1. Approve the proposal')
            print('2. Reject the proposal')
            adv_command = int(input(': '))
            if adv_command == 1:
                project_id = proposal_tb[0]['ProjectID']
                database.search('proposal_project').update(lambda x: x['ProjectID'] == project_id, 'Status', 'Approved')
                print('Approved proposal successfully.')
            elif adv_command == 2:
                project_id = proposal_tb[0]['ProjectID']
                database.search('proposal_project').update(lambda x: x['ProjectID'] == project_id, 'Status', 'Rejected')
                print('Rejected proposal successfully.')
            elif adv_command == 3:
                pass
            else:
                print('Invalid command')

    def run_menu(self):
        while True:
            self.menu()
            adv_command = int(input(': '))
            if adv_command == 1:
                self.check_details()
            elif adv_command == 2:
                self.check_proposal()
            elif adv_command == 0:
                print('logout successfully')
                print()
                break
            else:
                print('Invalid command')


class Admin:
    def __init__(self, adm_id):
        self.adm_id = adm_id

    @staticmethod
    def menu():
        print()
        print('Admin Menu')
        print('1. Show data')
        print('2. Add data')
        print('3. Delete data')
        print('4. Edit data')
        print('0. logout')

    @staticmethod
    def show_data():
        print()
        print('Select data')
        print('1. Person')
        print('2. Project')
        type_data = int(input(': '))
        if type_data == 1:
            person_data = database.search('person_table')
            person_tb = person_data.table
            print('    ID     |    fist     |    last     |    type    ')
            print('----------------------------------------------------')
            for row in person_tb:
                the_id = row['ID']
                fist = row['fist']
                last = row['last']
                the_type = row['type']
                print(f'{the_id:<14}{fist:<14}{last:<14}{the_type:<14}')
            print()
            input('[ Press "enter" to go back to the menu ]')
        elif type_data == 2:
            project_data = database.search('project_table')
            project_tb = project_data.table
            print(' ProjectID |    Title     |   Lead   |  Member1  |  Member2  |   Advisor  |   Status   ')
            print('---------------------------------------------------------------------------------------')
            for row in project_tb:
                project_id = row['ProjectID']
                title = row['Title']
                lead_id = row['Lead']
                mem1 = row['Member1']
                mem2 = row['Member2']
                adv = row['Advisor']
                status = row['Status']
                print(f'{project_id:<12}{title:<15}{lead_id:<11}{mem1:<12}{mem2:<12}{adv:<13}{status:<12}')
            print()
            input('[ Press "enter" to go back to the menu ]')
        else:
            print('Invalid command')

    @staticmethod
    def add_data():
        print()
        print('Select data')
        print('1. Person')
        print('2. Project')
        type_data = int(input(': '))
        if type_data == 1:
            while True:
                print('Fill in the data')
                print('! You have to fill in all these questions !')
                fist = input('Enter first name: ')
                last = input('Enter last name : ')
                the_type = input('Enter type of person : ')
                if fist != '' \
                        and last != '' \
                        and the_type != '':
                    # add data to person table
                    new_person = person_table_model.copy()
                    while True:
                        # generate password
                        the_id = f'{randrange(1, 10000000):07}'
                        check_id = database.search('login_table').filter(lambda x: x['ID'] == the_id)
                        if len(check_id.table) == 0:
                            break
                    new_person['ID'] = the_id
                    new_person['fist'] = fist
                    new_person['last'] = last
                    new_person['type'] = the_type
                    database.search('person_table').insert(new_person)
                    # add data to login table
                    new_login = login_table_model.copy()
                    new_login['ID'] = the_id
                    new_login['username'] = f'{fist}.{last[0]}'
                    while True:
                        # generate password
                        password = f'{randrange(1, 10000):04}'
                        check_pass = database.search('login_table').filter(lambda x: x['password'] == password)
                        if len(check_pass.table) == 0:
                            break
                    new_login['password'] = password
                    new_login['role'] = the_type
                    database.search('login_table').insert(new_login)
                    print('Add data successfully')
                    input('[ Press "enter" to go back to the menu ]')
                    break
                else:
                    print('Please fill in all the questions.')
                    print()
        elif type_data == 2:
            while True:
                print('Fill in the data')
                print('! You have to fill in all * question, others are optional !')
                title = input('* Enter the Title of the project : ')
                the_lead = input('* Enter leader ID : ')
                mem1 = input('Enter member1 ID : ')
                mem2 = input('Enter member2 ID : ')
                adv = input('Enter advisor ID : ')
                status = input('* Enter status : ')
                if title != '' \
                        and the_lead != '' \
                        and status != '':
                    while True:
                        # generate password
                        project_id = f'{randrange(1, 1000):04}'
                        check_id = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id)
                        if len(check_id.table) == 0:
                            break
                    new_project = project_table_model.copy()
                    new_project['ProjectID'] = project_id
                    new_project['Title'] = title
                    new_project['Lead'] = the_lead
                    new_project['Member1'] = mem1
                    new_project['Member2'] = mem2
                    new_project['Advisor'] = adv
                    new_project['Status'] = status
                    database.search('project_table').insert(new_project)
                    # update role to lead
                    database.search('person_table').update(lambda x: x['ID'] == the_lead, 'type', 'lead')
                    database.search('login_table').update(lambda x: x['ID'] == the_lead, 'role', 'lead')
                    if adv != '':  # update role to advisor
                        database.search('person_table').update(lambda x: x['ID'] == adv, 'type', 'advisor')
                        database.search('login_table').update(lambda x: x['ID'] == adv, 'role', 'advisor')
                    print('Add data successfully')
                    input('[ Press "enter" to go back to the menu ]')
                    break
                else:
                    print('Please fill in all * question')
                    print()
        else:
            print('Invalid command')

    @staticmethod
    def delete_data():
        print()
        print('Select data')
        print('1. Person')
        print('2. Project')
        type_data = int(input(': '))
        if type_data == 1:
            the_id = input('Enter person ID : ')
            person_data = database.search('person_table').filter(lambda x: x['ID'] == the_id)
            person_tb = person_data.table
            if not person_tb:
                print('ID not found.')
            else:
                database.search('person_table').delete(lambda x: x['ID'] == the_id)
                database.search('login_table').delete(lambda x: x['ID'] == the_id)
                print('Delete data successfully')
        elif type_data == 2:
            project_id = input('Enter project ID : ')
            project_data = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id)
            project_tb = project_data.table
            if not project_tb:
                print('ID not found.')
            else:
                database.search('project_table').delete(lambda x: x['ProjectID'] == project_id)
                print('Delete data successfully')

    @staticmethod
    def edit_data():
        print()
        print('Select data')
        print('1. Person')
        print('2. Project')
        type_data = int(input(': '))
        if type_data == 1:
            the_id = input('Enter person ID : ')
            print('( You cannot edit type/role column.)')
            column = input('Enter name of the column you want to edit : ')
            data = input('Enter new data : ')
            person_data = database.search('person_table').filter(lambda x: x['ID'] == the_id)
            person_tb = person_data.table
            column_list = ['ID', 'fist', 'last']
            if not person_tb:
                print('ID not found.')
            elif column not in column_list:
                print('Invalid column name.')
            else:
                database.search('person_table').update(lambda x: x['ID'] == the_id, column, data)
                if column == 'ID':
                    database.search('login_table').update(lambda x: x['ID'] == the_id, column, data)
                if column == 'fist' or 'last':
                    fist = person_tb[0]['fist']
                    last = person_tb[0]['last']
                    new_username = f'{fist}.{last[0]}'
                    database.search('login_table').update(lambda x: x['ID'] == the_id, 'username', new_username)
                print('Edit data successfully.')
                input('[ Press "enter" to go back to the menu ]')

        elif type_data == 2:
            project_id = input('Enter project ID : ')
            column = input('Enter name of the column you want to edit : ')
            data = input('Enter new data : ')
            project_data = database.search('project_table').filter(lambda x: x['ProjectID'] == project_id)
            project_tb = project_data.table
            column_list = ['ProjectID', 'Title', 'Lead', ' Member1', 'Member2', 'Advisor', 'Status']
            if not project_tb:
                print('project ID not found.')
            elif column not in column_list:
                print('Invalid column name.')
            else:
                database.search('project_table').update(lambda x: x['ProjectID'] == project_id, column, data)
                print('Edit data successfully')
                input('[ Press "enter" to go back to the menu ]')

    def run_menu(self):
        while True:
            self.menu()
            adm_command = int(input(': '))
            if adm_command == 1:
                self.show_data()
            elif adm_command == 2:
                self.add_data()
            elif adm_command == 3:
                self.delete_data()
            elif adm_command == 4:
                self.edit_data()
            elif adm_command == 0:
                print('logout successfully')
                print()
                break
            else:
                print('Invalid command')


# define a function called exit


def exit():
    writer = CSV()
    export_path = 'data/'
    writer.write(export_path + 'persons.csv', database.search('person_table').select('*'))
    writer.write(export_path + 'login.csv', database.search('login_table').select('*'))
    writer.write(export_path + 'project.csv', database.search('project_table').select('*'))
    writer.write(export_path + 'advisor_pending_request.csv', database.search('advisor_pending_request').select('*'))
    writer.write(export_path + 'member_pending_request.csv', database.search('member_pending_request').select('*'))
    writer.write(export_path + 'proposal_project.csv', database.search('proposal_project').select('*'))
    writer.write(export_path + 'evaluate.csv', database.search('evaluate').select('*'))


# here are things to do in this function:
# write out all the tables that have been modified to the corresponding csv files
# By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:

# https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


########################################################################################


initializing()

print('-- Welcome to Senior project managing program -- ')
while True:
    command = input('Enter the command (login / exit) : ')
    if command == 'exit':
        print('Exiting the program...')
        exit()
        break
    elif command == 'login':
        while True:
            val = login()
            if val is not None:
                break
        if val[1] == 'admin':
            admin = Admin(val[0])
            admin.run_menu()
        elif val[1] == 'student':
            student = Student(val[0])
            student.run_menu()
        elif val[1] == 'member':
            member = Member(val[0])
            member.run_menu()
        elif val[1] == 'lead':
            lead = Lead(val[0])
            lead.run_menu()
        elif val[1] == 'faculty':
            faculty = Faculty(val[0])
            faculty.run_menu()
        elif val[1] == 'advisor':
            advisor = Advisor(val[0])
            advisor.run_menu()
            pass
