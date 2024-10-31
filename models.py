from pydantic import BaseModel
 
class Usuario(BaseModel):
    id: str
    nombre: str
    email: str
    edad: int
 
 
class Proyecto(BaseModel):
    id: str
    nombre: str
    descripcion: str
    id_usuario: str