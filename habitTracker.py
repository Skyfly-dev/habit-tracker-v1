import json
from pathlib import Path
from datetime import date

BASE_DIR=Path(__file__).resolve().parent
FILE_PATH=BASE_DIR/"habits.json"


def load_data():
    """
    loads the habit tracker data from Json file.
    If the file is missing or corrupted ,it safely returns an empty database structure.
    """
    try:
        with open(FILE_PATH,"r") as file:
            data=json.load(file)
            return data

    except FileNotFoundError:
        return {"habits":[],"log":[]}
    except json.JSONDecodeError:
        return{"habits":[],"log":[]}



def save_data(data):
    """
    Saves the entire habit tracker dictionary in JSON file.
    """
    with open(FILE_PATH,"w") as file:
        json.dump(data,file,indent=4)



def find_habit_id(data,name):
    """
    translates a user provided habit name into its unique integer ID,
    Returns the ID if found ,otherwise returns None.
    """
    for item in data["habits"]:
        if name==item["name"]:
            return item["habit_id"]
    return None



def add_habit(data,name):
    """
    ADds a habit to the database with the next available id.
    prevent duplicate habits name.
    """
    if find_habit_id(data,name) is not None:
        print(f"Habit '{name}' already exists")
        return data
    
    habits=data["habits"]
    if not habits:
        new_id=1
    else:
        ids=[h["habit_id"] for h in habits ] #list comphrehension
        new_id=max(ids)+1
      
    habits.append({"habit_id":new_id,"name":name})
    return data




def get_today(data):
    """
    Calculate the status of evey habit foe the current date.
    returns a list of dictionaries:[{"name":"Gym","status":"done"},.....]
    """
    today=str(date.today())
    result=[]
    for habit in data["habits"]:
        status="not done"
        for entry in data["log"]:
            if habit["habit_id"]==entry["habit_id"] and entry["date"]==today:
                status=entry["status"]
                break
        result.append({"name":habit["name"],"status":status})

    return result




def print_today(data):
    """
    Prints a formatted view of todays habit to the terminal.
    """
    today_list=get_today(data)
    print("--- TODAY'S HABITS---")
    for item in today_list:
        print(f"{item['name']}:{item['status']}")

    return


    
def mark_habit(data,name,status):
    """
    Logs a habit as 'done' or 'skipped' for the current date.
    prevents logging the same habit twice on the same day.
    """
    habit_id=find_habit_id(data,name)
    if habit_id is None:
        print("Habit not found")
        return data
    today=str(date.today())
    #checked if already marked today
    for entry in data["log"]:
        if entry["habit_id"] ==habit_id and entry["date"]==today:
            print("Already marked for today!!") 
            return data
    data["log"].append({"habit_id":habit_id,"date":today,"status":status})

    return data 



def delete_habit(data,name):
    """
    Deletes a habit and all of its associate log entries(cascade delete)
    """
    habit_id=find_habit_id(data,name)
    if habit_id is None:
        print("Habit not found")
        return data

    #filters out deleted habit
    data["habits"]=[h for h in data["habits"] if h["habit_id"]!=habit_id]

    #filters out associate logs
    data["log"]=[l for l in data["log"] if l["habit_id"]!=habit_id]

    return data


    

def main():
    """
    the main CLI loop that handles user input.
    """
    data=load_data()
    while True:
        print("\n---HABIT TRACKER---")
        print("1. Add Habit")
        print("2. Mark Done")
        print("3. Mark Skip")
        print("4. View Today")
        print("5. Delete")
        print("6.Quit")

        choice=input("Enter choice: ")

        if choice=="1":
            name=input("Enter habit name: ")
            data=add_habit(data,name)
            save_data(data)
            print("successfully added!")

        elif choice=="2":
            name=input("Which habit did you do? ")
            data=mark_habit(data,name,status="done")
            save_data(data)
            print(f"habit ->{name} is marked done")

        elif choice=="3":
            name=input("Which habit you want to skip? ")
            data=mark_habit(data,name,status="skipped")
            save_data(data)
            print(f"habit ->{name} is marked skipped")
            
        elif choice=="4":
            print_today(data)

        elif choice=="5":
            name=input("which habit u wanna delete? ")
            delete_habit(data,name)
            print("deleted successfully")
            save_data(data)
            

        
        elif choice=="6":
            print("Goodbye!:) see u again......")
            break

        else:
            print("Invalid choice. Try again.")




if __name__=="__main__":
    main()