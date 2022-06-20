from fastapi import FastAPI
from dotenv import load_dotenv
from routes import user
from routes import authorize

#Project

from routes import dog
from starlette.middleware.cors import CORSMiddleware
from config.db import Base, engine



app = FastAPI()

load_dotenv()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], expose_headers=["*"]) #PERMITIMOS QUE LA API SEA ACCESIBLE DESDE TODOS LOS DOMINIOS

Base.metadata.create_all(bind=engine) #Permite crear las tablas de la base de datos


app.include_router(authorize.Route, prefix="/api")

app.include_router(dog.Route, prefix="/api/dogs")

app.include_router(user.Route, prefix="/api/users")



