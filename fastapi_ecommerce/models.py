from sqlalchemy import Column,Integer,String,Boolean
from database import base

class DBtask(base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True)
    description=Column(String)
    is_completed=Column(Boolean,default=False)

    