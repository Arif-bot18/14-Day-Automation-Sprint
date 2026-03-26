from fastapi import FastAPI , Depends
from pydantic import BaseModel #form validator 
from sqlalchemy import create_engine,Column,Integer,String #connects to the database,define the columns,data types 
from sqlalchemy.ext.declarative import declarative_base # creat the basetemplate for the database table
from sqlalchemy.orm import sessionmaker,Session #this create the conection to the databasd


Database_url = "sqlite:///./leads.db" #it's a connection string(address) or file 
engine = create_engine(Database_url,connect_args={"check_same_thread":False}) #it create a system that can create connection when needed or known how to connect

Sessionlocal = sessionmaker(autocommit = False,autoflush = False,bind = engine)#known how to create session using engine

Base = declarative_base() # it will create a blank template to design a table 

#creating the table 
class LeadTable(Base):
    __tablename__ = "Leads"
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String)
    email = Column(String)
    phone_no = Column(String)

Base.metadata.create_all(bind = engine)#base holds table designs and metadata collects them then create_all build them and engin tells where to build 

app = FastAPI()

class leadSchema(BaseModel):
    name:str
    email:str
    phone_no:int 




def get_db(): # this function is use to get database
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/leads")
def save_leads(package:leadSchema,db: Session = Depends(get_db)):
    new_lead = LeadTable(
        name = package.name,
        email = package.email,
        phone_no = package.phone_no)

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return {"message" :"save to sql","id":new_lead.id}    