import sys
import tkinter as tk

import weather as Weather

w = Weather()

avg_temp = lambda: w.query("SELECT AVG(temp) FROM weather")[0][0]
min_temp = lambda: w.query("SELECT MIN(temp) FROM weather")[0][0]
max_temp = lambda: w.query("SELECT MAX(temp) FROM weather")[0][0]
all_temp = lambda: w.query("SELECT temp FROM weather")

def gui():
	root = tk.Tk()

	w.get_forecast_plot(root)

	avgL = tk.Label(root);  avgL.pack()
	minL = tk.Label(root);  minL.pack()
	maxL = tk.Label(root);  maxL.pack()

	def set_labels():
		avgL.config(text=f"Averge  temperature: {avg_temp():.2f}")
		minL.config(text=f"Minimum temperature: {min_temp():.2f}")
		maxL.config(text=f"Maximum temperature: {max_temp():.2f}")

	def on_request_click():
		w.request_weather()
		set_labels()

	set_labels()

	tk.Button(root, text=f"Get K2 weather", command=on_request_click).pack(side=tk.BOTTOM)

	root.mainloop()

def helpcli():
	print("Syntax: weather_app CMD ARGS\n", file=sys.stderr)
	for k, v in cmds.items():
		print(f"{k} - {v[2]}; arguments: {v[1]}", file=sys.stderr)

cmds = {
	"alltemp": (all_temp,          0, "query all temperatures in data set"),
	"avgtemp": (avg_temp,          0, "query average temperature"   ),
	"forecast":(w.plot_forecast,   0, "perform forecast plot"       ),
	"gui":     (gui,               0, "launch gui version of this application"),
	"help":    (helpcli,           0, "display help"),
	"maxtemp": (max_temp,          0, "query maximum temperature"   ),
	"mintemp": (min_temp,          0, "query minimum temperature"   ),
	"request": (w.request_weather, 0, "request current weather data"),
}

if len(sys.argv) < 2:
	helpcli()
else:
	cmd = cmds[sys.argv[1]]
	func = cmd[0]
	argcount = cmd[1]
	result = func(*sys.argv[2:2+argcount])
	if result:
		print(result)

