from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import *
print('start')
engine = create_engine("sqlite:///cricket.db")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
print('done')