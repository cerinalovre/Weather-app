import requests
import config # Not necessary when 'config.api_key' is replaced with an actual API key
from tkinter import *
from tkinter import font
import tkinter.messagebox


API_KEY = config.api_key # API key available at https://openweathermap.org/, switch 'config.api_key' with an API key in string format.
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


root = Tk()

root.geometry('800x500')
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

    else:
        tkinter.messagebox.showerror(title='Error', message='An error ocurred')
        root.quit()
        
  
drop = OptionMenu(top_frame, clicked, *cities, command=display_selected)
drop_font = font.Font(size=12, weight='bold')
drop.config(width=15, height=2, font=drop_font)
drop.grid(row=0, column=0, pady=15)


root.mainloop()

