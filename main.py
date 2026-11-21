from fastapi import FastAPI
from habitTracker import load_data,save_data,add_habit,get_today,mark_habit,delete_habit,get_streak,get_history
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():

    return {"message":"Welcome to the Habit Tracker API"}


@app.get("/today")
def api_get_today():
    data=load_data()
    result=get_today(data)
    return result


class HabitCreate(BaseModel):
    name:str

class HabitMark(BaseModel):
    status:str

@app.post("/habits")
def api_add_habit(habit:HabitCreate):
    data=load_data()
    data=add_habit(data,habit.name)
    save_data(data)
    return {"message":f"Habit '{habit.name}' added successfully!"}


@app.post("/habits/{name}/mark")
def api_mark_habit(name:str,mark_data:HabitMark):
    data=load_data()
    data=mark_habit(data,name,mark_data.status)
    save_data(data)
    return {"message":f"Habit '{name}' marked as {mark_data.status} for today!"}



@app.delete("/habits/{name}")
def api_delete_habit(name:str):
    data=load_data()
    data=delete_habit(data,name)
    save_data(data)
    return {"message":f"Habit '{name}' deleted successfully!"}



@app.get("/habits/{name}/streak")
def api_get_streak(name:str):
    data=load_data()
    streak_value=get_streak(data,name)
    return {"habit":name ,"streak":streak_value}


@app.get("/habits/{name}/history")
def api_get_history(name:str,days:int=7):
    data=load_data()
    history_data=get_history(data,name,days)
    return {"habit":name,"history":history_data}