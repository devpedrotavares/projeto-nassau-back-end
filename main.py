from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
import dotenv
from models import Animal
from models import Cliente
from typing import List

dotenv.load_dotenv()

class Canil:
    def __init__(self):
        self.conexao = psycopg2.connect(user=os.environ['FDB_user'],
                                  password=os.environ['FDB_password'],
                                  host=os.environ['FDB_host'],
                                  port=os.environ['FDB_port'],
                                  database=os.environ['FDB_database'])
        self.cursor = self.conexao.cursor()


    def selectfull(self):
        self.cursor.execute("SELECT id,nome,raca,vacinado,castrado,idade FROM ANIMAIS")
        return self.cursor.fetchall()

    def selectwhere(self,id):
        self.cursor.execute(f"SELECT * FROM ANIMAIS WHERE ID = '{id}'")
        return self.cursor.fetchall()

    def selectoneuser(self, email, password):
        self.cursor.execute(f"SELECT * FROM CLIENTES WHERE email = '{email}' AND senha = '{password}'")
        return self.cursor.fetchone()

    def getlastinsertedid(self):
        self.cursor.execute(f"SELECT ID FROM ANIMAIS ORDER BY ID DESC")
        return self.cursor.fetchone()

    def delete(self,id):
        try:
            self.cursor.execute(f"DELETE FROM ANIMAIS WHERE ID = '{id}'")
            self.conexao.commit()
        except:
            self.conexao.rollback()

    def insertclient(self,email,password):
        try:
            self.cursor.execute(f"INSERT INTO CLIENTES(email,senha) VALUES('{email}','{password}')")
            self.conexao.commit()
        except:
            self.conexao.rollback()

    def insertanimal(self,nome,raca,vacinado,castrado,idade):
        try:
            self.cursor.execute(f"INSERT INTO ANIMAIS(nome,raca,vacinado,castrado,idade) VALUES('{nome}','{raca}','{vacinado}','{castrado}','{idade}')")
            self.conexao.commit()
        except:
            self.conexao.rollback()

canil = Canil()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login/")
async def login(cliente: Cliente):
    user = canil.selectoneuser(cliente.email,cliente.password)
    if(user is None):
        canil.insertclient(cliente.email,cliente.password)
        return {"isAdmin": False}

    return {"isAdmin": user[3]}
    
@app.get("/animais")
def animais():
    print(canil.selectfull()) 
    return canil.selectfull()

    
@app.get("/animais/{id}")
def animal(id: int):
    return canil.selectwhere(id)


@app.post("/cadanimal/")
async def cadanimal(animal: Animal):
    print(animal)
    canil.insertanimal(animal.nome,animal.raca,animal.vacinado,animal.castrado,animal.idade)
    return {"id": canil.getlastinsertedid()}

@app.get("/delanimal/{id}")
def delete(id: int):
    return canil.delete(id)