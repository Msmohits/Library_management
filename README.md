                                        # Library_management

#Requirements: library management system based on provided scenario Candidates have to implement web REST api's for each required 
              action related to scenario Proper JWT based authentication should be implemented in each protected web api endpoint
              Ensure an user can only perform actions using apis which are allowed to the role assigned to that user Scenario 
              The are two roles in the system LIBRARIAN and MEMBER  As a User I can signup either 


#Login : as LIBRARIAN and MEMBER using username and password I can login using username/password and get JWT access token 

#LIBRARIAN: As a Librarian I can add, update, and remove Books from the system I can add, update, view, and remove Member from the system,also Books_status 

#MEMBER: As a Member I can view, borrow, and return available Books Once a book is borrowed, its status will change to BORROWED Once a book is returned, 
        its status will change to AVAILABLE I can delete my own account

                                        # Backend Task

search for a user by name.
sort list by field name.
pagination of users list.
get detailed user.


                                        # Steps to start project

pip install virtualenv			    (install virtual environment)
python -m venv venv                 (create vietual environment)
source venv/bin/activate		    (activate environment))

sudo apt-get install build-essential autoconf libtool pkg-config python3-dev libssl-dev libmysqlclient-dev python3-venv libpq-dev python3-psycopg2

pip install -r requirements.txt		(install project dependencies)

python manager.py runserver		    (to start application)
