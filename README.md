
# LED Matrix Weather Station

This is a weather station I have coded for an Adafruit LED matrix, for the Hack Club Neon program. It is coded in CircuitPython, and uses the OpenWeatherMap API and assets. The font is a modified version of "5x7 practical".


## Features

- Displays current date and time
- Displays temperature in degrees Celsius
- Displays wind speed in miles per hour
- Displays high and low temperatures in degrees Celsius
- Displays icon dynamically fetched from OpenWeatherMap to represent weather
- Updates weather data every 2 minutes

## Demo

You can view a demo of the project by copy-pasting the code into this website:
[https://neon.hackclub.dev/editor](https://neon.hackclub.dev/editor)

You will also have to upload the font file to the website.

On line 14, edit the text inside the quotation marks to show the name of the city you wish to lookup, and the two letter country code (check [here](https://openweathermap.org/find) to see if your city is valid)

On line 15, put your OpenWeatherMap API key inside the square brackets, then delete the square brackets (should look like this: `url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=yourapikeygoeshere&units=metric'.format(city)`)

![Demo screenshot]()

