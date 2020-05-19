from tkinter import *
from Asteroid import Asteroid
import json
import requests
import datetime

#This is a function that creates the url for the json to retrieve data from
def dateManip(startDate, endDate):
    beginString = 'https://api.nasa.gov/neo/rest/v1/feed?start_date='
    midString = '&end_date='
    endString = '&api_key=WBEFL37pGfFEfovgShjGKOtlyBydg3Dbd7HQdcK1'
    datestring = beginString + startDate + midString + endDate + endString
    print(datestring)
    return(datestring)

#This function resets any buttons for asteroids called in 
# previous uses and creates new ones based on the parameters 
# inputted into the text boxes
def callAsteroid():
        for widget in center.winfo_children():
                widget.destroy()
        center.grid(row=0, sticky="ew")
        startDate = str(textbox1.get())
        endDate = str(textbox2.get())
        dateRange = dateManip(startDate, endDate)
        response = requests.get(dateRange)
        json_data = response.json()
        asteroids_data = json_data.get('near_earth_objects')
        results = []
        for date in asteroids_data:
                for asteroid in asteroids_data[date]:
                        results.append(Asteroid(asteroid["id"], asteroid['name'], asteroid['close_approach_data'][0]['relative_velocity']['miles_per_hour'], asteroid['close_approach_data'][0]['miss_distance']['miles'], asteroid['nasa_jpl_url']))
        i = 0
        for asteroid in results:
                Button(center, text="Details", command=asteroid.specifyAsteroid).grid(row=i, column = 0)
                Label(center, text= asteroid.id, width=10, pady=1, padx=1).grid(row=i, column = 1)
                Label(center, text= asteroid.name, width=10, pady=1, padx=1).grid(row=i, column = 2)
                Label(center, text= asteroid.miles_per_hour, width=10, pady=1, padx=1).grid(row=i, column = 3)
                Label(center, text= asteroid.miles, width=20, pady=20, padx=1).grid(row=i, column = 4)
                Label(center, text= asteroid.url, width=40, pady=20, padx=1).grid(row=i, column = 5)          
                i += 1
        

        return

#This is the Tk Frame for the input box, where the parameters
# are inputted into textboxes and results are gotten
#  based on said parameters
root = Tk()
root.title('Model Definition')
root.geometry('{}x{}'.format(300, 90))

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# create all of the main containers
top_frame = Frame(root, bg='cyan',padx=3, pady=3)


top_frame.grid(row=0, sticky="ew")


# create the widgets for the top frame
label1 = Label(top_frame, text="Start Date:")
textbox1 = Entry(top_frame)
label2 = Label(top_frame, text="End Date:")
textbox2 = Entry(top_frame)
button1 = Button(top_frame, text="Filter", bg="Blue", fg="White", command = callAsteroid)

# layout the widgets in the top frame
label1.grid(row=0, column=0, sticky=E)
textbox1.grid(row=0, column=1)
label2.grid(row=1, column=0, sticky=E)
textbox2.grid(row=1, column=1)
button1.grid(row=2, column=0)

#This is a separate Tk for the list of asteroids
#It will get reset with each iteration of callAsteroid
asteroidList = Tk()
asteroidList.title('Asteroids')
asteroidList.geometry('{}x{}'.format(900, 800))
asteroidList.grid_rowconfigure(1, weight=1)
asteroidList.grid_columnconfigure(0, weight=1)
center = Frame(asteroidList, bg='white',padx=3, pady=3)
center.grid(row=0, sticky="ew")

root.mainloop()
