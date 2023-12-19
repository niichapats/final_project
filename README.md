# Final project for 2023's 219114/115 Programming I

### List of file

#### folder data

- person.csv - contains all person data
- login.csv - contains login data
- member_pending_request.csv - contains data about requesting member for the project
- advisor_pending_request.csv - contains data about requesting advisor for the project
- project.csv - contains all project data except member request status and advisor request status
- proposal_project.csv - contains proposal data
- evaluate.csv - contains evaluation data

#### main

- Proposal.md - description how the program works
- TODO.md - a list of things to do
- model.py - contains all models that were used in this project (all keys)
- database.py - contains classes and methods that were used in project_mange.py  

**Class and its method (database.py)**

| Class | Method | Action                                                                                         |
|-------|--------|------------------------------------------------------------------------------------------------|
| CSV   | init   | Initializes a CSV object with a file path                                                      |
| CSV   | read   | Reads data from the specified CSV file and returns a list of dictionaries                      |
| CSV   | write  | Writes data to the specified CSV file                                                          |
| DB    | init   | Initializes a DB object with an empty list to store tables                                     |
| DB    | insert | Inserts a table into the database                                                              |
| DB    | search | Searches for a table in the database by name                                                   |
| Table | init   | Initializes a Table object with a name and data                                                |
| Table | filter | generates a new table with rows filtered from the current table based on a provided condition  |
| Table | join   | Creates a new table by joining with another table on specified keys                            |
| Table | select | Selects specific attributes from the table                                                     |
| Table | delete | Deletes rows from the table that satisfy the given condition                                   |
| Table | insert | Inserts a new entry (dictionary) into the table                                                |
| Table | update | Updates values in the table for rows that satisfy the given condition                          |


- project_manage.py - contains 6 classes(all roles) and 3 functions(initializing, login, exit)
  - Function
    - initializing
       - Read all .csv and insert to be a table
    - login
       -  Function checks user-entered credentials against a 'login_table' in the database. If valid, it returns the user's ID and role; otherwise, it prints an error and returns None.
    - exit
       - Stop running the program and save changes of all data in csv file
  - Class
    - Student
        - Manages student-related actions and contains all the relevant methods for creating projects and checking requests.
    - Lead
        - Manages lead student-related actions and contains all the relevant methods for sending member requests, checking pending member status, requesting an advisor, checking pending advisor status, sending a proposal, sending the project, checking the project status and checking the project details.
    - Member
        - Manages member-related actions and contains all the relevant methods for checking pending member status, checking pending advisor status, checking the project status and checking the project details.
    - Faculty
        - Manages faculty-related actions and contains all the relevant methods for checking advisor requests and evaluating the project.
    - Advisor
      - Manages advisor-related actions and contains all the relevant methods for checking the project details and checking and approving a proposal. 
    - Admin
      - Manages admin-related actions and contains all the relevant methods for showing data, adding data, deleting data and editing data.


### Role and its function

| Role    | Action                                                                                                  | Method                                                    | Class   | Completion Percentage |
|---------|---------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|---------|-----------------------|
| Student | Check if there are any member requests sent to this student, then choose to accept or deny the request  | check_request, accept_request, deny_request               | Student | 100%                  |
| Student | Check if this student already has a project. If not, create a new project                               | create_project                                            | Student | 100%                  |
| Lead    | Send a member request to other students                                                                 | send_request                                              | Lead    | 100%                  |
| Lead    | Show the pending member status (waiting, accept, deny)                                                  | pending_member_status, get_project_id                     | Lead    | 100%                  |
| Lead    | Send a advisor request to faculties                                                                     | request_advisor, get_project_id                           | Lead    | 100%                  |
| Lead    | Show the pending advisor status (waiting, accept, deny)                                                 | pending_advisor_status, get_project_id                    | Lead    | 100%                  |
| Lead    | Send a proposal to their own advisor                                                                    | send_proposal, get_project_id, get_role_id                | Lead    | 100%                  |
| Lead    | Send the project to the evaluator(randomly from the faculty)                                            | send_project, get_project_id, get_role_id                 | Lead    | 100%                  |
| Lead    | Show the project status(proposal status, project evaluation)                                            | check_status                                              | Lead    | 100%                  |
| Lead    | Show all the details of the project                                                                     | check_details, get_name                                   | Lead    | 100%                  |
| Member  | Show the pending member status (waiting, accept, deny)                                                  | pending_member_status, get_project_id                     | Member  | 100%                  |
| Member  | Show the pending advisor status (waiting, accept, deny)                                                 | pending_advisor_status, get_project_id                    | Member  | 100%                  |
| Member  | Send the project to the evaluator(randomly from the faculty)                                            | check_status                                              | Member  | 100%                  |
| Member  | Show all the details of the project                                                                     | check_details, get_nam                                    | Member  | 100%                  |
| Faculty | Check if there are any advisor requests sent to this faculty, then choose to accept or deny the request | check_request, accept_request_adv, deny_request, get_name | Faculty | 100%                  |
| Faculty | Check if there are any project evaluation request, then evaluate the project(approve, reject)           | evaluate, get_name                                        | Faculty | 100%                  |
| Advisor | Show all the details of the project this advisor is advising on                                         | check_details, get_name                                   | Advisor | 100%                  |
| Advisor | Check if there are any proposal sent to this advisor, then choose to accept or reject the proposal      | check_proposal                                            | Advisor | 100%                  |
| Admin   | Show all data in the table(choose person / project table)                                               | show_data                                                 | Admin   | 100%                  |
| Admin   | Add data to person table / project table                                                                | add_data                                                  | Admin   | 100%                  |
| Admin   | Delete data in person table / project table                                                             | delete_data                                               | Admin   | 75%   **              |
| Admin   | Edit data in  person table / project table                                                              | edit_data                                                 | Admin   | 75%   ***             |

** Can delete only in person table, login table, project table. (not all the related tables)  
*** Can choose only some column to edit, update only person login table and project table (not all the related tables)


### How to compile and run the project
- Run project_manage.py
- Login by username and password, then the program will show the menu that your role can do
- Select any option you want to do
- When you finish everything, logout(by enter 0) and exit the program


### Missing features and outstanding bugs

Bugs : I have fixed all the bugs I found.  
Missing Features : These are all features I think I should add more
- Member : modify project information
- Faculty and Advisor : show all projects details
- Advisor : add comments about the project him/her is advising on
