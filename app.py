import streamlit as st
import requests

#url of backend
API_URL="http://127.0.0.1:8000"

#page title + browser tab text 
st.set_page_config(page_title="Habit Tracker", page_icon="🔥")
st.title("🔥HABIT TRACKER")


#side bar -add a new habit
st.sidebar.header("Add a New Habit")
new_habit=st.sidebar.text_input("Habit Name")
if st.sidebar.button("Add Habit"):
    if new_habit:
        #send a post req to fastapi
        response=requests.post(f"{API_URL}/habits",json={"name":new_habit})
        if response.status_code==200:
            st.sidebar.success(f"Added '{new_habit}' !")
        else:
            st.sidebar.error("Failed to add habit.")
    else:
        st.sidebar.warning("Please enter a name. ")

#Main page:showing todaya habits
st.header("Today's Habits")

#Send a get request to fastapi
response=requests.get(f"{API_URL}/today")
if response.status_code==200:
    today_habits=response.json()
    if today_habits:
        for habit in today_habits:
            #create 6 colmns name,stus,done button,skip ,delete button ....streak button
            col1,col2,col3,col4,col5,col6=st.columns([2,1,1,1,1,1])
            col1.markdown(f"**{habit['name']}**")

            #show the current status nicely
            if habit["status"]=="done":
                col2.success("Done")
            elif habit["status"]=="skipped":
                col2.warning("skipped")
            else:
                col2.error("Not Done")


            #streak logic
            #ask fastaoi for streak for specific habit
            streak_response=requests.get(f"{API_URL}/habits/{habit['name']}/streak")
            if streak_response.status_code==200:
                streak_data=streak_response.json()
                streak_value=streak_data["streak"]

                #if streak is 0,just show 0 
                if streak_value>0:
                    col3.write(f"🔥**{streak_value}**")
                else:
                    col3.write("0")
            else:
                col3.write("-") #fallback if api fails


            #button to mark a done
            if col4.button("❤️",key=f"done_{habit['name']}"):
                requests.post(f"{API_URL}/habits/{habit['name']}/mark",json={"status":"done"})
                st.rerun() #refresh to show new status


            #button to mark skipped
            if col5.button("💔",key=f"skip_{habit['name']}"):
                requests.post(f"{API_URL}/habits/{habit['name']}/mark" , json={"status":"skipped"})
                st.rerun()

            #delete button(NEW)
            if col6.button("🗑️",key=f"delete_{habit['name']}"):
                requests.delete(f"{API_URL}/habits/{habit['name']}")
                st.rerun()
    else:
        st.info("No habits for today.Add some at the sidebar!")



        #chart section
    st.divider()
    st.header("📊 Last 7 days History")
    habit_names=[h['name'] for h in today_habits]

    if habit_names:
            selected_habit=st.selectbox("Select a habit to view its chart",habit_names)

            days_to_show=st.slider("How many days do you want to see?",min_value=3,max_value=30,value=7)

            if selected_habit:
                history_response=requests.get(f"{API_URL}/habits/{selected_habit}/history")
                if history_response.status_code==200:
                    history_data=history_response.json()["history"]

                    st.bar_chart(history_data,color="#FF4B4B")
                    
                else:
                    st.error("Could not load history data. 😔")

    else:
                st.info("Add some habits first to see the chart ☺️!")
