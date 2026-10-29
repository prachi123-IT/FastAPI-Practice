from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
import models
from database import engine,get_db

app=FastAPI(title="Practice")

items_db={1:"Laptop",2:"Smartphone",3:"WirlessHeadphones"}

@app.get("/")
def home():
    return{"message":"Hello world!"}

#path parameter
@app.get("/greet/{name}/{age}")
def check_age(name:str,age:int):
    if age>=18:
        return {"Message":f"Welcome abroad, {name}! you are allowed in"}

    return{"Message":f"Sorry {name}!,you must be 18 or older"}

#query parameter
@app.get("/search/{item_id}")
def get_item(item_id:int,search_query:str=None,discount:bool=False):
    item_name=items_db.get(item_id,"Unknown Item")
    return {
        "requested_id":item_id,
        "item_found":item_name,
        "search_filter":search_query,
        "apply_discount":discount
    }

#requestbody using pydantic
class productschema(BaseModel):
    name:str=Field(min_length=2,max_length=30)
    price:float=Field(gt=0.0)
    category:str="General"

@app.post("/add-product")
def create_product(product:productschema):
    product_dict=product.model_dump()
    product_dict["id"]=101
    return {"message":"Success!","Saved_data":product_dict}

#response model
class userSignup(BaseModel):
    username:str
    email:str
    password:str

class userResponse(BaseModel):
    id:int
    username:str
    email:str

@app.post("/register",response_model=userResponse)
async def register_user(user_in:userSignup):
    db_user_row={
        "id":55,
        "username":user_in.username,
        "email":user_in.email,
        "password":user_in.password
    }
    return db_user_row 

#nested response body
class address(BaseModel):
    city:str
    pincode:int
class userProfile(BaseModel):
    name:str
    email:str
    address_i:address

@app.get("/user-profile",response_model=userProfile)
async def get_profile():
    raw_data={
        "name": "rahul_coder",
        "email": "rahul@example.com",
        "address_i": {
            "city": "Indore",
            "pincode": 452001
        }
    }
    return raw_data


#database connection
models.base.metadata.create_all(bind=engine)

class taskcreate(BaseModel):
    title:str
    description:str
@app.post("/task/add")
async def add_new(task_input:taskcreate,db:Session=Depends(get_db)):
    new_db=models.DBtask(
        title=task_input.title,
        description=task_input.description,
        is_completed=False
    )
    db.add(new_db)
    db.commit()
    db.refresh(new_db)

    return{"message":"saved successfully!","task_id":new_db}

@app.get("/tasks/all")
async def read_all_tasks(db:Session=Depends(get_db)):
    all_task=db.query(models.DBtask).all()
    return all_task