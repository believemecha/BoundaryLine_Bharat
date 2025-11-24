from fastapi import FastAPI
from fastapi import Depends

# from sqlalchemy.orm import Session


# from .database import *  
# from engine.storage.models import *  

# Import controller modules
import app.controllers.batsman_stats_controller as batsman_stats_controller
import app.controllers.players_controller as players_controller


# Base.metadata.create_all(bind=engine)

app = FastAPI()


#Register Controller modules here

app.include_router(batsman_stats_controller.router)
app.include_router(players_controller.router)



@app.get("/")
def get_players():
    return {"hey": "I am here!"}

@app.get("/up")
def health_check():
    return {"status": "healthy"}
