# EstudoPython

1- Install Python

2- Install VScode

3- Install Virtual Environment using VScode Terminal

      py -3 -m venv <name>
      
  ex: py -3 -m venv venv
  
4- Select Phyton Interpreter (View-> Command Pallet -> Select Interpreter) and select ".\venv\Scripts\python.exe"

5- Active Virtual Environment on VSCode Terminal

    Type and Run "venv\Scripts\activate.bat"
    
6- Install FastAPI Package with all optional dependencies

    pip install fastapi[all]
    
7- Look and extract the dependencies

    pip freeze > requirements.txt
    
8- Run localy the app

    uvicorn app.main:app --reload

9- Install libs sqlalchemy and pymysql for working with mysql

    pip install sqlalchemy pymysql

10- Remember to redo step 7 on every change on libs

11- Install xampp for working with mysql localy

    https://www.apachefriends.org/pt_br/index.html

12- Install passlib and Bcrypt for hashing passwords

    pip install passlib[bcrypt]

13- Install python-jose and cryptography for working with jwt token

    pip install python-jose[cryptography]

14- Install alembic a migration db tool

    pip install alembic

15- Create tables using alembic

    alembic init alembic
    alembic revision -m "create post table"
    alembic revision -m "create users table"

16- Create new revision autogenarated

    alembic revision --autogenerate -m "auto generate db changes"

