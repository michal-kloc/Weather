import time

import weather as Weather

w = Weather()

while True:
	w.request_weather()
	print(f"Request performed ({time.ctime()})")
	time.sleep(w.T)

