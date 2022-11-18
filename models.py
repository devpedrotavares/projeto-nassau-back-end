from pydantic import BaseModel

class Cliente(BaseModel):
    email: str
    password: str

class Animal(BaseModel):
    nome: str
    raca: str
    vacinado: bool
    castrado: bool
    idade: int