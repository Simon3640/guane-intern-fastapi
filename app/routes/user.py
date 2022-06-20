from typing import List
from fastapi import APIRouter, Response, UploadFile, status, File
from fastapi.responses import JSONResponse
from sqlalchemy import table
from schemas.dog import responseDog
from models.user import modelUser
from config.querys import get_all, get_one_user, create_object, delete_user, update_user, dogs_by_user, put_file

from schemas.user import User, responseUser

Route=APIRouter()
table = modelUser.__table__

#Path operation que permite obtener todos los usuarios de la base de datos
@Route.get(
    '/',
    response_model=List[responseUser],
    summary="Get all users",
    tags = ["users"]
    )
async def get_users():
    """
    Path operation for get all users in database
    
    this path operation dont reiceve any parameters
    
    Returns:
    
        List[modelUser]: List of users
    """
    response = await get_all(table)
    return response


#Path operation que permite obtener un usuario de la base de datos
@Route.get(
    '/{id}',
    response_model=responseUser,
    summary="Get user by id",
    tags = ["users"]
    )
async def get_user(id: int):
    """
    Path operation for get user by id
    
    Args:
    
        id: id of user
    
    Returns:
    
        modelUser: user
    """
    response = await get_one_user(table, id)
    return response

#Este endpoint nos devuelve los perros adoptados por el usuario con id id
@Route.get(
    '/dogs/{id}',
    response_model=List[responseDog],
    summary="Get dogs by user id",
    tags = ["dogs"]
)
async def get_dogs_by_user(id: int):
    """
    Path operation for get dogs adopted by user id
    
    Args:
    
        id: id of user
    
    Returns:
    
        List[modelDog]: List of dogs
    """
    response = await dogs_by_user(id)
    return response


#Este endpoint nos permite crear un nuevo usuario
@Route.post(
    '/',
    status_code = status.HTTP_201_CREATED,
    summary="Create user",
    tags = ["users"]
    )
async def create_user(user: User):
    """
    Path operation for create user
    
    This path operation receive a user object as JSON:
    
        name: name of user
        last_name: last name of user
        email: email of user

    
    Returns:
    
        modelUser: user created
    """
    await create_object(table, user.dict())
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created"})

    


#Este endpoint nos permite actualizar el usuario con id id
@Route.put(
    '/{id}',
    status_code=status.HTTP_200_OK,
    summary="Update user",
    tags = ["users"]
    )
async def updateUser(id: int, user: User):
    """
    Path operation for update user
    
    Args:
    
        id: id of user
        user as JSON:
            name : name of user
            last_name : last name of user
            email : email of user
    
    Returns:
    
        modelUser: user updated
    """
    await update_user(table, id, user.dict())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User updated"})


#Este endpoint permite eliminar el usuario con id id
@Route.delete(
    '/{id}',
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    description="Delete user information",
    tags = ["users"]
    )
async def deleteUser(id: int):
    """
    Path operation for delete user
    
    Args:
    
        id: id of user
    
    Returns:
    
        modelUser: user deleted
    """
    await delete_user(table, id)
    return JSONResponse({"message": "User deleted"},200)


#TODO: Pongo esto aquí para no poner una ruta para un único path operation
@Route.post(
    '/file',
    status_code=status.HTTP_200_OK,
    summary="Get file",
    tags = ["file"]
    )
async def get_file():
    """
    Path operation for get file
    
    Args:
      
        file: file to get
    
    Returns:
      
        UploadFile: file
    """
    response = await put_file()
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
