from fastapi import FastAPI, HTTPException, Query, Path
from typing import List, Optional
from models import Usuario, Proyecto
from azure.cosmos import exceptions
from datetime import datetime
from database import container_usuario,container_proyecto

app = FastAPI(title='API de Gestion de Usuarios y proyectos')

###USUARIOS###
#Crear usuario POST
@app.post("/usuarios/", response_model=Usuario, status_code=201)
def create_usuario(usuario: Usuario):
    try:
        container_usuario.create_item(body=usuario.dict())
        return usuario
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El usuario con este ID ya existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))    
    
#Obtener usuario GET
@app.get("/usuarios", response_model=List[Usuario])
def get_usuarios():
    query = "SELECT * FROM c"
    items = list(container_usuario.query_items(query = query, enable_cross_partition_query=True))
    return items

#Actualizar usuario PUT
@app.put("/usuarios/{usuario_id}", response_model=Usuario)
def update_usuario(usuario_id:str, updated_usuario: Usuario):
    try:
        existing_usuario = container_usuario.read_item(item=usuario_id, partition_key=usuario_id)
        existing_usuario.update(updated_usuario.dict(exclude_unset=True))
        container_usuario.replace_item(item=usuario_id, body=existing_usuario)
        return existing_usuario
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encotrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Eliminar usuario DELETE
@app.delete("/usuarios/{usuario_id}", status_code=204)
def delete_usuario(usuario_id: str):
    try:
        container_usuario.delete_item(item=usuario_id, partition_key=usuario_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

###PROYECTOS###
#Crear proyecto POST
@app.post("/proyectos/",response_model=Proyecto, status_code=201)
def add_proyecto(proyecto: Proyecto):
    try:
        usuario = container_usuario.read_item(item=proyecto.id_usuario, partition_key=proyecto.id_usuario)
        container_proyecto.create_item(body=proyecto.dict())
        return proyecto
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=400, detail="Evento no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Listar Proyectos GET
@app.get("/proyectos/", response_model=List[Proyecto])
def Listar_Proyectos():
    query = "SELECT * FROM c"
    items = list(container_proyecto.query_items(query=query, enable_cross_partition_query=True))
    return items

#Listar Proyectos por usuario GET
@app.get("/proyectos/{id_usuario}", response_model=List[Proyecto])
def Listar_Proyectos(id_usuario: str):
    query = f"SELECT * FROM c WHERE c.id_usuario= '{id_usuario}'"
    items = list(container_proyecto.query_items(query=query, enable_cross_partition_query=True))
    return items

#Actualizar proyecto PUT
@app.put("/proyecto/{proyect_id}", response_model=Proyecto)
def update_proyecto(proyect_id:str, updated_usuario: Proyecto):
    try:
        existing_proyecto = container_proyecto.read_item(item=proyect_id, partition_key=proyect_id)
        existing_proyecto.update(updated_usuario.dict(exclude_unset=True))
        container_proyecto.replace_item(item=proyect_id, body=existing_proyecto)

        return existing_proyecto
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encotrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#Eliminar proyecto DELETE
@app.delete("/proyecto/{proyect_id}", status_code=204)
def delete_proyecto(proyect_id: str):
    try:
        container_proyecto.delete_item(item=proyect_id, partition_key=proyect_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail='Proyecto no encontrado')
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))