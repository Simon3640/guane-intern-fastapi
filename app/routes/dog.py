
from fastapi import APIRouter, Body, Header, Query, Response, status
from fastapi.responses import JSONResponse
from celery_worker import create_task
from functions_jwt import validate_token
from config.querys import get_one, get_all, get_dogs_adopted, update_dog, delete_dog, get_picture
from typing import Optional, List
from models.dog import modelDog
from schemas.dog import Dog, responseDog

table = modelDog.__table__ #Tabla de perros para ingresar como parámetro a las funciones de querys

Route = APIRouter()

#Path operation que permite obtener todos los perros de la base de datos
@Route.get(
    "/",
    response_model=List[responseDog],
    summary="Get all dogs",
    tags=["dogs"]
    )
async def get_dogs():
    """
    Path operation for get all dogs in database

        this path operation dont reiceve any parameters

    Returns

        List[modelDog]: List of dogs

    """
    response = await get_all(table)
    return response




#Este endpoint nos devuelve los perros adoptados
@Route.get(
    "/is_adopted",
    response_model=List[responseDog],
    summary="Get all dogs that are adopted",
    tags=["dogs"]
    )
async def dogs_adopted():
    """
    Path operation for get all dogs that are adopted

    returns:

        List[Dog]: List of dogs that are adopted
    
    """
    response = await get_dogs_adopted()
    return response


#Este endpoint nos devuelve el PRIMER perro con nombre name
@Route.get(
    "/{name}",
    response_model=responseDog,
    summary="Get dog by name",
    tags=["dogs"]
    )
async def get_dog(name: str):
    """
    Path operation for get dog by name

    Args:

        name: name of dog

    returns:

        Dog: dog information
    """
    response = await get_one(table, name)
    if response is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Dog not found"})
    return response


#Esta es la única path operation que le asigné un worker de celery, es lo que se pide en la prueba
@Route.post(
    "/{name}",
    status_code = status.HTTP_201_CREATED,
    summary="Create a dog",
    tags=["dogs"]
    )
async def post_dog(
    name: str,
    adopted: Optional[bool] = Query(False, description="Is the dog adopted?"),
    auth : str = Header(None),
    s : Optional[int] = Query(0, description="Delay in seconds")
    ):
    """
    Path operation for create a dog
    
    Args:

        name: name of dog
        adopted: is the dog adopted?
        s: delay in seconds
        auth: token of user
    
    returns:

        Dog: dog information
    """
    validation_response = validate_token(auth, output=False) #Se hace esto pues solo me piden validar el ingreso del canino nuevo
    if validation_response == None:
        
        picture = await get_picture()
        
        data = {
            "name": name,
            "is_adopted": adopted*1,
            "picture": picture
        }

        response = create_task.apply_async((data , s), countdown=s)
        response = response.get()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Dog created"})
    else:
        return validation_response




#Estpath operation permite actualizar el PRIMER perro con nombre name
@Route.put(
    "/{name}",
    status_code = status.HTTP_200_OK,
    summary="Update a dog",
    tags=["dogs"]
    )
async def putDog(
    dog : Dog = Body(description="Dog to update"),
    name : str = Query(None, description="Name of dog to update"),
    ):
    """
    Path operation for update a dog
    
    Args:

        dog as JSON: 
            name: name of dog if have new name
            is_adopted: is the dog adopted?
            user_id: id of user
            created_date: date of creation
            picture: picture of dog
        name: name of dog to update
    
    returns:

        Response: response with status code 200 if dog was updated
    """
    await update_dog(table, name, dog.dict())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Dog updated"})



#Estpath operation permite eliminar el PRIMER perro con nombre name
@Route.delete(
    "/{name}",
    status_code = status.HTTP_200_OK,
    summary="Delete a dog",
    tags=["dogs"]
    )
async def deleteDog(name: str):
    """
    Path operation for delete a dog
    
    Args:

        name: name of dog to delete
    
    returns:

        Response: response with status code 200 if dog was deleted
    """
    await delete_dog(table, name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Dog deleted"})