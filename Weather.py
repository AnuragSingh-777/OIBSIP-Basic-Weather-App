import tkinter as tk
from tkinter import ttk
import requests

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x600")

        # Create a main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill="x")

        self.location_label = tk.Label(self.header_frame, text="Location:")
        self.location_label.pack(side="left")

        self.location_entry = tk.Entry(self.header_frame, width=50)
        self.location_entry.pack(side="left")

        self.get_weather_button = tk.Button(self.header_frame, text="Get Weather", command=self.get_weather)
        self.get_weather_button.pack(side="left")

        self.clear_button = tk.Button(self.header_frame, text="Clear", command=self.clear_data)
        self.clear_button.pack(side="left")

        self.exit_button = tk.Button(self.header_frame, text="Exit", command=self.root.destroy)
        self.exit_button.pack(side="left")

        self.current_weather_frame = tk.Frame(self.main_frame)
        self.current_weather_frame.pack(fill="x")

        self.current_weather_label = tk.Label(self.current_weather_frame, text="", wraplength=700)
        self.current_weather_label.pack(fill="x")

        self.hourly_forecast_frame = tk.Frame(self.main_frame)
        self.hourly_forecast_frame.pack(fill="both", expand=True)

        self.hourly_forecast_label = tk.Label(self.hourly_forecast_frame, text="Hourly Forecast:")
        self.hourly_forecast_label.pack(fill="x")

        self.hourly_forecast_tree = ttk.Treeview(self.hourly_forecast_frame)
        self.hourly_forecast_tree["columns"] = ("Time", "Temperature", "Weather")
        self.hourly_forecast_tree.column("#0", width=0, stretch="no")
        self.hourly_forecast_tree.column("Time", anchor="w", width=150)
        self.hourly_forecast_tree.column("Temperature", anchor="w", width=100)
        self.hourly_forecast_tree.column("Weather", anchor="w", width=200)
        self.hourly_forecast_tree.heading("#0", text="", anchor="w")
        self.hourly_forecast_tree.heading("Time", text="Time", anchor="w")
        self.hourly_forecast_tree.heading("Temperature", text="Temperature", anchor="w")
        self.hourly_forecast_tree.heading("Weather", text="Weather", anchor="w")
        self.hourly_forecast_tree.pack(fill="both", expand=True)

    def get_weather(self):
        # Get the weather data
        location = self.location_entry.get()
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(base_url)
        weather_data = response.json()

        if "weather" in weather_data and "main" in weather_data and "wind" in weather_data:
            current_weather = weather_data["weather"][0]["description"]
            current_temp_kelvin = weather_data["main"]["temp"]
            current_temp_celsius = current_temp_kelvin - 273.15
            wind_speed = weather_data["wind"]["speed"]

            self.current_weather_label.config(text=f"Current Weather: {current_weather}\nTemperature: {current_temp_celsius:.2f}°C\nWind Speed: {wind_speed} m/s")

            hourly_forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}"
            hourly_forecast_response = requests.get(hourly_forecast_url)
            hourly_forecast_data = hourly_forecast_response.json()

            self.hourly_forecast_tree.delete(*self.hourly_forecast_tree.get_children())
            for i, forecast in enumerate(hourly_forecast_data["list"]):
                time = forecast["dt_txt"]
                temp_kelvin = forecast["main"]["temp"]
                temp_celsius = temp_kelvin - 273.15
                weather = forecast["weather"][0]["description"]
                self.hourly_forecast_tree.insert("", "end", values=(time, f"{temp_celsius:.2f}°C", weather))

    def clear_data(self):

        self.current_weather_label.config(text="")

        self.hourly_forecast_tree.delete(*self.hourly_forecast_tree.get_children())

        self.location_entry.delete(0, "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
