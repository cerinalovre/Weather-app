import requests
import config # Not necessary when 'config.api_key' is replaced with an actual API key
from tkinter import *
from tkinter import font
import tkinter.messagebox
from PIL import Image, ImageTk
import datetime


API_KEY = config.api_key # API key available at https://openweathermap.org/, switch 'config.api_key' with an API key in string format.
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


curr_time = datetime.datetime.now()

root = Tk()

root.geometry('700x500')
root.title('Weather App')

important_font = font.Font(size=20, weight='bold')
normal_font = font.Font(size=14)

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
  
clicked = StringVar()
clicked.set("Choose a city")

def display_selected(city):
    for widget in bottom_frame.winfo_children():
        widget.destroy()

    city = clicked.get()
    request_url = f'{BASE_URL}?appid={API_KEY}&q={city}'
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
       
        city_label = Label(bottom_frame, text=city, font=important_font)
        city_label.grid(row=0, sticky=W)
        temp_label = Label(bottom_frame, text=str(round(data['main']['temp']-273.15))+'°C', font=important_font)
        temp_label.grid(row=1, sticky=W)
        humidity_label = Label(bottom_frame, text='Humidity: '+str(data['main']['humidity'])+'%', font=normal_font)
        humidity_label.grid(row=2, sticky=W)
        pressure_label = Label(bottom_frame, text='Pressure: '+str(data['main']['pressure'])+' hPa', font=normal_font)
        pressure_label.grid(row=3, sticky=W)
        visibility_label = Label(bottom_frame, text='Visibility: '+str(data['visibility']//1000)+' km', font=normal_font)
        visibility_label.grid(row=4, sticky=W)
        padding_label = Label(bottom_frame, text='')
        padding_label.grid(row=5, pady=30)

        weather_type = data['weather'][0]['id']

        if weather_type>199 and weather_type<233:
            icon_url = 'weather_icons\thunder.png'

        if weather_type>299 and weather_type<322:
            icon_url = 'weather_icons\light_rain.png'

        if weather_type>499 and weather_type<532:
            icon_url = 'weather_icons\heavy_rain.png'

        if weather_type>599 and weather_type<623:
            icon_url = 'weather_icons\snow.png'
        
        if weather_type>700 and weather_type<782:
            icon_url = 'weather_icons\fog.png'

        if weather_type == 800:
            if curr_time.hour>19 and curr_time.hour<6:
                icon_url = 'weather_icons\clear_moon.png'
            else:
                icon_url = 'weather_icons\clear_sun.png'

        if weather_type == 801 or weather_type == 802:
            if curr_time.hour>19 and curr_time.hour<6:
                icon_url = 'weather_icons\clouds_night.png'
            else:
                icon_url = 'weather_icons\clouds_day.png'

        if weather_type == 803 or weather_type == 804:
            icon_url = 'weather_icons\clouds.png'

        weather_label = Label(bottom_frame, text='Weather: '+data['weather'][0]['description'], font=normal_font)
        weather_label.grid(row=0, column=1, padx=30)

        photo = PhotoImage(file=icon_url)
        icon_label = Label(bottom_frame, image=photo, borderwidth=2, relief="solid")
        icon_label.image = photo # Keeping a reference to the object, otherwise icon is blank :(
        icon_label.grid(column=1, row=1, rowspan=4, padx=50)

    else:
        tkinter.messagebox.showerror(title='Error', message='An error ocurred')
        root.quit()
        
  
drop = OptionMenu(top_frame, clicked, *cities, command=display_selected)
drop_font = font.Font(size=12, weight='bold')
drop.config(width=15, height=2, font=drop_font)
drop.grid(row=0, column=0, pady=30)


root.mainloop()

