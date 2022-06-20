import time
from celery import Celery, shared_task
from models.dog import modelDog
from config.db import engine

celery = Celery(__name__,
                broker='redis://redis:6379/0',
                backend='redis://redis:6379/0')


#Creamos de esta manera el worker unicamente por ser una base de datos con solo dos tablas, en caso de tener multiples tablas se debe implementar de una manera más eficiente
@shared_task(name = "create_task")
def create_task(data : dict, a= 0):
    time.sleep(a)
    with engine.connect() as conn:
         conn.execute(modelDog.__table__.insert().values(data))
    return {'message': 'SUCCESS'}