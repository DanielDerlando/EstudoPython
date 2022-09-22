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
