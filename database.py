from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,text

engine = create_engine("postgresql+psycopg2://postgres:Tribe666%40@localhost:5432/task_manager")

sessionlocal = sessionmaker(bind=engine)

