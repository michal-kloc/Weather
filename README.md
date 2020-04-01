# Intro

Are you a group of crude daredevils, who totally professionally, yes,
forgot to check the weather just 3 days before your flight to Islamabad?

Well, LUCKY YOU.

We, at the best company here, that shall not be named (mostly because I am
to lazy to make the name up) care about ~~money~~ your safety so much, that
we decided to make this app! The best possible app\* for your needs on your
way to the top of mighty K2!

# Weather

__Weather__ is small project written in Python, which can be used to retrieve
weather data from [openweathermap](https://openweathermap.org/).

# Project structure

## weather.py

Defines class which reads configuration, creates database (if doesn't exist)
and provides list of utility functions to ease database operations and
connecting.

#### usage:

```python
import weather

w = weather() # configuration is loaded from current directory

# or

w = weather(custom_config)
```

#### functions:

```python
@staticmethod
def data_to_query_tuple(data):
	"Converts query result into database-compatible tuple."
```

```python
def __init__(self, config=None):
	"Loads configuration and creates database if doesn't exist"
```

```python
def request_weather(self):
	"""Query https://openweathermap.org/ for current weather
	data and store it in database."""
```

```python
def plot_forecast(self):
	"Query https://openweathermap.org/ for forecast.
```

```python
def query(self, query, args=None):
	"Query the database. Returns all fetched results."
```

```python
def __dbinit(self):
	"Private, create database"
```

```python
def __insert(self, data):
	"Private, insert record into database"
```

```python
def __request_forecast(self):
	"Private, Request forecast data"
```

```python
def __url(self, rtype):
	"Private, constructs url to query with."
```

## weather\_deamon.py

Not an actual daemon, although should be used like one. This script, when
launched, queries periodically [openweathermap](https://openweathermap.org/) for current
weather data and stores it in database.

#### usage:

```sh
python3 weather_daemon.py

# or

python3 weather_daemon.py &
```

## weather\_api.py
Weather project __entry__, can be used to query database for weather statistics
and to plot forecast.

#### usage:

```sh
python3 weather_api.py CMD ARGS
```

#### CMDs:

- __alltemp__  - query all temperatures in data set
- __avgtemp__  - query average temperature
- __forecast__ - erform forecast plot
- __gui__      - launch gui version of this application
- __help__     - display help
- __maxtemp__  - query maximum temperature
- __mintemp__  - query minimum temperature
- __request__  - request current weather data

## config.json

Project configuration.

- __key__: [openweathermap](https://openweathermap.org/) access key
- __lat__, __lon__: monitored location coordinates
- __units__: units to receive results in
- __db\_name__: database file name
- __T__: period in which __weather\_daemon__ performs requests

# Bugs

Not very well tested!

# Sidenotes

\* I mean, probably. Not. No refunds.

