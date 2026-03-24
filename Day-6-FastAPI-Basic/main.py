from fastapi import FastAPI 
from datetime import datetime

app = FastAPI()
@app.get("/")
def get_status():
    return{
        "message" : "Automation API online"
    }
@app.get("/status")
def get_server_time():
    server_time = datetime.now().strftime("%I:%M %p")
    return {"time":server_time}