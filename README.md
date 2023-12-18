# Final project for 2023's 219114/115 Programming I

### List of file

##### folder data

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

| Class | Method | Action                                                                    |
|-------|--------|---------------------------------------------------------------------------|
| CSV   | init   | Initializes a CSV object with a file path                                 |
| CSV   | read   | Reads data from the specified CSV file and returns a list of dictionaries |
| CSV   | write  | Writes data to the specified CSV file                                     |
| DB    | init   | Initializes a DB object with an empty list to store tables                |
| DB    | insert | Inserts a table into the database                                         |
| DB    | search | Searches for a table in the database by name                              |
| Table | init   | Initializes a Table object with a name and data                           |
| Table | join   | Creates a new table by joining with another table on specified keys       |
| Table | select | Selects specific attributes from the table                                |
| Table | delete | Deletes rows from the table that satisfy the given condition              |
| Table | insert | Inserts a new entry (dictionary) into the table                           |
| Table | update | Updates values in the table for rows that satisfy the given condition     |


- project_manage.py - contains 6 classes(all roles) and 3 functions(initializing, login, exit)
  1. initializing
     - Read all .csv and insert to be a table
  2. login
     -  function checks user-entered credentials against a 'login_table' in the database. If valid, it returns the user's ID and role; otherwise, it prints an error and returns None.
  3. exit
     - stop running the program and save changes of all data in csv file

**Role and its function (project_manage.py)**

| Role    | Action                                                                                                  | Method                 | Class   | Completion Percentage |
|---------|---------------------------------------------------------------------------------------------------------|------------------------|---------|-----------------------|
| Student | Check if there are any member requests sent to this student, then choose to accept or deny the request  | check_request          | Student | 100%                  |
| Student | Check if this student already has a project. If not, create a new project                               | create_project         | Student | 100%                  |
| Lead    | Send a member request to other students                                                                 | send_request           | Lead    | 100%                  |
| Lead    | Show the pending member status (waiting, accept, deny)                                                  | pending_member_status  | Lead    | 100%                  |
| Lead    | Send a advisor request to faculties                                                                     | request_advisor        | Lead    | 100%                  |
| Lead    | Show the pending advisor status (waiting, accept, deny)                                                 | pending_advisor_status | Lead    | 100%                  |
| Lead    | Send a proposal to their own advisor                                                                    | send_proposal          | Lead    | 100%                  |
| Lead    | Send the project to the evaluator(randomly from the faculty)                                            | send_project           | Lead    | 100%                  |
| Lead    | Show the project status(proposal status, project evaluation)                                            | check_status           | Lead    | 100%                  |
| Lead    | Show all the details of the project                                                                     | check_details          | Lead    | 100%                  |
| Member  | Show the pending member status (waiting, accept, deny)                                                  | pending_member_status  | Member  | 100%                  |
| Member  | Show the pending advisor status (waiting, accept, deny)                                                 | pending_advisor_status | Member  | 100%                  |
| Member  | Send the project to the evaluator(randomly from the faculty)                                            | check_status           | Member  | 100%                  |
| Member  | Show all the details of the project                                                                     | check_details          | Member  | 100%                  |
| Faculty | Check if there are any advisor requests sent to this faculty, then choose to accept or deny the request | check_request          | Faculty | 100%                  |
| Faculty | Check if there are any project evaluation request, then evaluate the project(approve, reject)           | evaluate               | Faculty | 100%                  |
| Advisor | Show all the details of the project this advisor is advising on                                         | check_details          | Advisor | 100%                  |
| Advisor | Check if there are any proposal sent to this advisor, then choose to accept or reject the proposal      | check_proposal         | Advisor | 100%                  |
| Admin   | Show all data in the table(choose person / project table)                                               | show_data              | Admin   | 100%                  |
| Admin   | Add data to person table / project table                                                                | add_data               | Admin   | 100%                  |
| Admin   | Delete data in person table / project table                                                             | delete_data            | Admin   | 75%   **              |
| Admin   | Edit data in  person table / project table                                                              | edit_data              | Admin   | 75%   ***             |

** Can delete only in person table, login table, project table. (not all the related tables)  
*** Can choose only some column to edit, update only person login table and project table (not all the related tables)


#### How to compile and run the project
- Run project_manage.py
- Login by username and password, then the program will show the menu that your role can do
- Select any option you want to do
- When you finish everything, logout(by enter 0) and exit the program


#### Missing features and outstanding bugs

Bugs : I have fixed all the bugs I found.  
Features : These are all features I think I should add more
- Member : modify project information
- Faculty and Advisor : show all project details
- Advisor : add comment
