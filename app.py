from tkinter import *
from tkinter import font
import tkinter.messagebox
import datetime

import requests


API_KEY = 'c19d186a0add032f9dc1b6f86036db84'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


root = Tk()

IMPORTANT_FONT = font.Font(size=20, weight='bold')
NORMAL_FONT = font.Font(size=14)
DROPDOWN_FONT = font.Font(size=12, weight='bold')
CURRENT_TIME = datetime.datetime.now()

root.geometry('700x500')
root.title('Weather App')

top_frame = Frame(root)
top_frame.pack(side=TOP)
bottom_frame = Frame(root)
bottom_frame.pack(side=BOTTOM)

cities = [
    "Zagreb",
    "Split",
    "Rijeka",
    "Osijek",
    "Zadar",
    "Dubrovnik",
    "Pula"
]

def weather_icon_type(weather_type):
        if weather_type>199 and weather_type<233:
            icon_url = 'weather_icons\thunder.png'

        elif weather_type>299 and weather_type<322:
            icon_url = 'weather_icons\light_rain.png'

        elif weather_type>499 and weather_type<532:
            icon_url = 'weather_icons\heavy_rain.png'

        elif weather_type>599 and weather_type<623:
            icon_url = 'weather_icons\snow.png'
        
        elif weather_type>700 and weather_type<782:
            icon_url = 'weather_icons\fog.png'

        elif weather_type == 800:
            if CURRENT_TIME.hour>19 and CURRENT_TIME.hour<6:
                icon_url = 'weather_icons\clear_moon.png'
            else:
                icon_url = 'weather_icons\clear_sun.png'

        elif weather_type == 801 or weather_type == 802:
            if CURRENT_TIME.hour>19 and CURRENT_TIME.hour<6:
                icon_url = 'weather_icons\clouds_night.png'
            else:
                icon_url = 'weather_icons\clouds_day.png'

        elif weather_type == 803 or weather_type == 804:
            icon_url = 'weather_icons\clouds.png'

        return icon_url


def display(city):
    for widget in bottom_frame.winfo_children(): # Clearing the bottom frame every time a new city is selected to
        widget.destroy()                         # prevent text being displayed on top of the previous one.

    city = clicked.get()
    request_url = f'{BASE_URL}?appid={API_KEY}&q={city}'
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
       
        city_label = Label(bottom_frame, text=city, font=IMPORTANT_FONT)
        city_label.grid(row=0, sticky=W)

        temp_label = Label(bottom_frame, text=str(round(data['main']['temp']-273.15)) + '°C', font=IMPORTANT_FONT)
        temp_label.grid(row=1, sticky=W)

        humidity_label = Label(bottom_frame, text='Humidity: ' + str(data['main']['humidity']) + '%', font=NORMAL_FONT)
        humidity_label.grid(row=2, sticky=W)

        pressure_label = Label(bottom_frame, text='Pressure: ' + str(data['main']['pressure']) + ' hPa', font=NORMAL_FONT)
        pressure_label.grid(row=3, sticky=W)

        visibility_label = Label(bottom_frame, text='Visibility: ' + str(data['visibility']//1000) + ' km', font=NORMAL_FONT)
        visibility_label.grid(row=4, sticky=W)

        weather_label = Label(bottom_frame, text='Weather: ' + data['weather'][0]['description'], font=NORMAL_FONT)
        weather_label.grid(row=0, column=1, padx=30)

        padding_label = Label(bottom_frame, text='')
        padding_label.grid(row=5, pady=30)

        weather_type = data['weather'][0]['id']
        icon_url = weather_icon_type(weather_type)
        photo = PhotoImage(file=icon_url)
        icon_label = Label(bottom_frame, image=photo, borderwidth=2, relief="solid")
        icon_label.image = photo # Keeping a reference to the object, otherwise icon is blank
        icon_label.grid(column=1, row=1, rowspan=4, padx=50)

    else:
        tkinter.messagebox.showerror(title='Error', message='An error ocurred')
        root.quit()

clicked = StringVar()
clicked.set("Choose a city")
         
drop = OptionMenu(top_frame, clicked, *cities, command=display)
drop.config(width=15, height=2, font=DROPDOWN_FONT)
drop.grid(row=0, column=0, pady=30)

root.mainloop()

