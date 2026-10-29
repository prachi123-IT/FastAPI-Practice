# create_engine: Imports the engine manager. It manages the low-level network connections to the database file or server.
# sessionmaker: Imports a factory creator. It lets us create database conversation session pipelines.
# declarative_base: Imports the foundation layer class. It bridges your Python classes directly to database columns.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

database_url="sqlite:///./my_app.db"
# DATABASE_URL = "postgresql://username:password@localhost:5432/my_database_name"
# DATABASE_URL = "mysql+pymysql://root:pass@localhost:3306/prod_db"

engine=create_engine(database_url,connect_args={"check_same_thread":False},echo=True)
# The connect_args={"check_same_thread": False} setting is a special safety key required only for SQLite. It lets multiple fast, asynchronous FastAPI workers talk to the local file at the same time without hitting file locks.

sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
#autocommit=False: Prevents the database from saving things instantly before your code tells it to confirm.
#autoflush=False: Stops SQLAlchemy from sending early changes to the database before you are fully ready

base=declarative_base()

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()