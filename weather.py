import json
import matplotlib.pyplot as plt
import os
import requests
import sqlite3
import sys

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

URL_SERVER = "http://api.openweathermap.org/data/2.5"

class Weather:

	__slots__ = ["db_name", "key", "lat", "lon", "T", "units"]

	@staticmethod
	def data_to_query_tuple(data):
		main = data["main"]
		wind = data["wind"]
		return (
			data["dt"],
			main["temp"],
			main["feels_like"],
			main["temp_min"],
			main["temp_max"],
			main["pressure"],
			main["humidity"],
			main["sea_level"],
			main["grnd_level"],
			wind["speed"],
			wind["deg"],
			data["clouds"]["all"],
		)

	def __init__(self, config=None):

		if config == None:
			f = open("config.json")
			config = json.load(f)
			f.close()

		self.db_name = config["db_name"]
		self.key = config["key"]
		self.lat = config["lat"]
		self.lon = config["lon"]
		self.T = config["T"]
		self.units = config["units"]

		if not os.path.isfile(self.db_name):
			self.__dbinit()

	def __dbinit(self):
		conn = sqlite3.connect(self.db_name)
		c = conn.cursor()

		c.execute("""CREATE TABLE weather (
			dt               UNSIGNED INT PRIMARY KEY,
			temp             REAL,
			temp_feels_like  REAL,
			temp_min         REAL,
			temp_max         REAL,
			pressure         REAL,
			humidity         REAL,
			sea_level        REAL,
			grnd_level       REAL,
			wind_speed       REAL,
			wind_deg         REAL,
			clouds           REAL
		)""")

		conn.commit()
		conn.close()

	def __insert(self, data):
		conn = sqlite3.connect(self.db_name)
		c = conn.cursor()

		c.execute(f"""INSERT INTO weather VALUES
			(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

		conn.commit()
		conn.close()

	def __request_forecast(self):
		response = requests.get(self.__url("forecast")) # TODO: check status code?
		data = json.loads(response.content.decode("utf-8"))
		data = data["list"]

		x = [d["dt"] for d in data]
		y = [d["main"]["temp"] for d in data]
		xlabels = [d["dt_txt"] for d in data[::6]]

		return x, y, xlabels

	def __url(self, rtype):
		return f"{URL_SERVER}/{rtype}?lon={self.lon}&lat={self.lat}&units={self.units}&APPID={self.key}"

	def request_weather(self):
		response = requests.get(self.__url("weather")) # TODO: check status code?
		data = json.loads(response.content.decode("utf-8"))
		self.__insert(Weather.data_to_query_tuple(data))

	def plot_forecast(self):
		x, y, xlabels = self.__request_forecast()
		plt.scatter(x, y, marker="o", s=30)
		plt.xticks(x[::6], xlabels)
		plt.xlabel("date", labelpad=20, fontsize=24)
		plt.ylabel("$^\\circ C$", labelpad=30, fontsize=24)
		plt.title("Temperature forecast", fontsize=24)
		#plt.tight_layout()
		plt.show()

	def get_forecast_plot(self, root):
		x, y, xlabels = self.__request_forecast()

		figure = plt.Figure(figsize=(16, 8), dpi=100)
		ax = figure.add_subplot(111)
		ax.scatter(x, y, marker="o", s=30)
		ax.set_xticks(x[::6])
		ax.set_xticklabels(xlabels, fontsize=10)
		ax.set_xlabel("date", labelpad=20, fontsize=24)
		ax.set_ylabel("$^\\circ C$", labelpad=30, fontsize=24)
		ax.set_title("Temperature forecast", fontsize=24)
		#ax.tight_layout()
		scatter = FigureCanvasTkAgg(figure, root)
		scatter.get_tk_widget().pack()

	def query(self, query, args=None):
		conn = sqlite3.connect(self.db_name)
		c = conn.cursor()

		if args:
			c.execute(query, args)
		else:
			c.execute(query)

		result = c.fetchall()
		conn.close()

		return result

sys.modules[__name__] = Weather

