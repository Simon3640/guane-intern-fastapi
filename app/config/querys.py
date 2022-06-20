from config.db import engine
from httpx import AsyncClient

#Este documento nos permite consultar, insertar, actualizar y eliminar elementos de la base de datos

#Esta función nos permite consultar todos los elementos de alguna tabla de la base de datos
async def get_all(table):
    """get_all function
    This function get all data from a table

    Args:
        table: table to get data from

    Returns:
        [List]: list of data from table
    """
    with engine.connect() as conn:
        return conn.execute(table.select()).fetchall()


#Esta funcieon nos permite obtener la información de un perro de la base de datos
#!Una mejor manera de hacer esto para hacerlo más eficiente es buscar por id, pues pueden existir mas de dos perros con el mismo nombre
async def get_one(table, name):
    """get_one function

    Args:
        table (Sqalchemy Table): table to get data from
        name (str): name of the object to get

    Returns:
        Object: return information of the first dog with the name provided
    """
    with engine.connect() as conn:
        return  conn.execute(table.select().where(table.c.name == name)).fetchone()



#Esta función permite obtener un usuario de la base de datos
# * Notemos que esta función es extendible para todo tipo de tabla
async def get_one_user(table, id):
    """get_one_user function

    Args:
        table (Sqalchemy Table): table to get data from
        id (int): id of the object to get

    Returns:
        [object]: return information of the object with the id provided
    """
    with engine.connect() as conn:
        return  conn.execute(table.select().where(table.c.id == id)).fetchone()


#Esta función permite obtener todos los perros que están en estado adoptado
async def get_dogs_adopted():
    """get_dogs_adopted function

    Returns:
        [List[Dogs]]: list of dogs with the status adopted
    """
    with engine.connect() as conn:
        return  conn.execute('SELECT * FROM dogs WHERE is_adopted = 1').fetchall()


#Esta función permite insertar un nuevo objeto en la base de datos, es extendible a todo tipo de objetos
async def create_object(table, data : dict):
    """create_object function

    Args:
        table (Sqalchemy Table): Table to insert data in
        data (dict): data to insert in the table
    """
    with engine.connect() as conn:
        conn.execute(table.insert().values(data))


#Esta función permite actualizar un perro de la tabla
#!Esta función es super problematica, porque actualiza la información de multiples perros con el mismo nombre, es por esto que la manera correcta de hacerlo es buscar por id pero para seguir los lineamientos de la prueba se hace así
#? La manera correcta de hacerlo es primero generar un query para buscar por nombre y posteriormente seleccionar por id en el fron-end
async def update_dog(table, name : str, dict : dict):
    """update_dog function with problematic way!!!!!!!!!!

    Args:
        table (Sqalchemy): Table to update data in 
        name (str): name of the dog to update
        dict (dict): data to update in the table
    """
    with engine.connect() as conn:
        conn.execute(table.update().values(dict).where(table.c.name == name))


#Esta función en comparación con la anterior si es si es extendible a todo tipo de tablas, pues se trabaja por id
async def update_user(table, id : int, dict : dict):
    """update_user function

    Args:
        table (Sqalchemy Table): table to update data in
        id (int): id of the object to update
        dict (dict): data to update in the table
    """
    with engine.connect() as conn:
        conn.execute(table.update().values(dict).where(table.c.id == id))


#Esta función permite eliminar un perro según el criterio nombre
#! Super problemática por lo que se ha mensionado hasta ahora
async def delete_dog(table, name: str):
    """delete_dog function

    Args:
        table (Sqalchemy Table): table to delete data from
        name (str): name of the object to delete
    """
    with engine.connect() as conn:
        conn.execute(table.delete().where(table.c.name == name))


#Esta función si es extendible y permite eliminar un usuario de la base de datos
async def delete_user(table, id : int):
    """" delete_user function

    Args:
        table (Sqalchemy Table): table to delete data from
        id (int): id of the object to delete
    """
    with engine.connect() as conn:
        conn.execute(table.delete().where(table.c.id == id))



#Esta función es extra con respecto a los lineamientos de la prueba, permite consultar los perros que han sido adoptados por el usuario con id user_id
async def dogs_by_user(user_id : int):
    """dogs_by_user function

    Args:
        user_id (int): id of the user to get dogs from

    Returns:
        [List[Dogs]]: list of dogs adopted by the user with the id provided

    """
    with engine.connect() as conn:
        return  conn.execute('SELECT * FROM dogs WHERE user_id = {}'.format(user_id)).fetchall()
    

#Esta función  es la que consulta en la api que devuelve la url de una imágen de un perro
async def get_picture():
    """get_picture function

    Returns:
        str: url of the picture
    """
    async with AsyncClient() as client:
        response = await client.get("https://dog.ceo/api/breeds/image/random")
        return response.json()["message"]



#Esta función sube un binario a la API de Guane
async def put_file():
    """put_file function
    
    Returns:
        str: '{
            "filename" : "guane_upload" 
        }'
    """
    async with AsyncClient() as client:
        files = {'file': b'Estoy aplicando a Guane'}
        response = await client.post("https://gttb.guane.dev/api/files", files=files)
        return response.text