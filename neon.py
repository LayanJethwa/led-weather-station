import adafruit_display_text.label
import adafruit_bitmap_font.bitmap_font
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import requests
import math
from PIL import Image
from io import BytesIO

city = "Loughborough, GB"
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2600288cd7cff5584c34b20cedb6dc72&units=metric'.format(city)
data = ''

font = adafruit_bitmap_font.bitmap_font.load_font("5x7 practical-11-r.bdf")

default_colour = 0xFFFFFF
neutral_colour = 0xB6BCBE
wind_scale = [0xff0000, 0xff3700, 0xff5000, 0xff6200, 0xff7200, 0xfc8200, 0xf49500, 0xeaa700, 0xdab900, 0xc9c900, 0xb2da00, 0x89ec00, 0x00ff00]
temp_scale = [0x0000d6, 0x0019d4, 0x0027d3, 0x0031d1, 0x0039d0, 0x0041ce, 0x0049cb, 0x004fc9, 0x0156c7, 0x0a5bc5, 0x1361c3, 0x1b66c0, 0x226bbe, 0x2a6fbc, 0x3074b9, 0x3778b6, 0x3d7cb4, 0x4380b1, 0x4984af, 0x4f88ac, 0x558ca9, 0x5a90a6, 0x6093a3, 0x6597a0, 0x6b9a9d, 0x719e99, 0x76a196, 0x7ca492, 0x81a88f, 0x87ab8b, 0x8cae87, 0x91b183, 0x97b47e, 0x9cb77a, 0xa1ba75, 0xa6bd70, 0xacc06a, 0xb1c364, 0xb6c65d, 0xbbc855, 0xc1cb4d, 0xc6ce43, 0xcbd136, 0xd1d325, 0xd6d600,
             0xd72100, 0xd93100, 0xda3e00, 0xdb4800, 0xdc5200, 0xdd5b00, 0xde6300, 0xde6b00, 0xdf7200, 0xdf7a00, 0xdf8100, 0xdf8800, 0xdf8f00, 0xdf9500, 0xdf9b00, 0xdfa100, 0xdfa800, 0xdeae00, 0xddb300, 0xddb900, 0xdcbf00, 0xdac500, 0xd9cb00, 0xd8d000, 0xd6d600]

def beaufort_scale(num):
    if num<1:
        return 12
    elif num<4:
        return 11
    elif num<8:
        return 10
    elif num<13:
        return 9
    elif num<19:
        return 8
    elif num<25:
        return 7
    elif num<32:
        return 6
    elif num<39:
        return 5
    elif num<47:
        return 4
    elif num<55:
        return 3
    elif num<64:
        return 2
    elif num<73:
        return 1
    else:
        return 0

def num_size(num):
    size = 0
    for i in range(len(num)):
        if num[i] == '.' :
            size += 4
        elif num[i] == '1':
            size += 2
        else:
            size += 5

        if i != len(num)-1:
            size += 1
    return size

def get_image(code):
    response = requests.get(f"https://openweathermap.org/img/wn/{code}.png")
    image = Image.open(BytesIO(response.content)).convert('RGBA').resize((25,25))
    pixel_data = image.getdata()
    image_bitmap = displayio.Bitmap(25,25,1024)
    image_palette = displayio.Palette(1024)
    for i, colour in enumerate(pixel_data):
        image_bitmap[i%25, i//25] = i
        image_palette[i] = (colour[0],colour[1],colour[2])
    return displayio.TileGrid(image_bitmap, pixel_shader=image_palette, x=42, y=11)

def get_weather():
    global data
    res = requests.get(url)
    data = res.json()
    print(data)

get_weather()

current_time = [str(i) for i in time.localtime(time.time())]
date_string = current_time[2].zfill(2)+"/"+current_time[1].zfill(2)+"/"+current_time[0].zfill(4)
time_string = current_time[3].zfill(2)+":"+current_time[4].zfill(2)+":"+current_time[5].zfill(2)

# Release old displays
displayio.release_displays()

# Create led matrix
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Groups

g1 = displayio.Group()
display.root_group = g1

g1.append(get_image(data["weather"][0]["icon"]))

date_text = adafruit_display_text.label.Label(
         font,
        color=neutral_colour,
        text = date_string)
date_text.x = 0
date_text.y = 3
g1.append(date_text)

time_text = adafruit_display_text.label.Label(
         font,
        color=neutral_colour,
        text = time_string)
time_text.x = 0
time_text.y = 11
g1.append(time_text)

temp_text = adafruit_display_text.label.Label(
         font,
        color=temp_scale[math.floor(data["main"]["temp"])+30],
        text = str(round(data["main"]["temp"],1))+" C")
temp_text.x = 0
temp_text.y = 20
g1.append(temp_text)

degree_text = adafruit_display_text.label.Label(
         font,
        color=temp_scale[math.floor(data["main"]["temp"])+30],
        text = ".")
degree_text.x = num_size(str(round(data["main"]["temp"],1)))+1
degree_text.y = 14
g1.append(degree_text)

wind_text = adafruit_display_text.label.Label(
         font,
        color=wind_scale[beaufort_scale(data["wind"]["speed"])],
        text = str(round(data["wind"]["speed"]))+"mph")
wind_text.x = 0
wind_text.y = 28
g1.append(wind_text)

high_text = adafruit_display_text.label.Label(
         font,
        color=0xFF0000,
        text = str(round(data["main"]["temp_max"])))
high_text.x = 35
high_text.y = 20
g1.append(high_text)

low_text = adafruit_display_text.label.Label(
         font,
        color=0x0000FF,
        text = str(round(data["main"]["temp_min"])))
low_text.x = 35
low_text.y = 28
g1.append(low_text)

seconds = 0

icons = [1,2,3,4,9,10,11,13,50]
dn = ['d','n']

while True:
    #g1[0] = get_image(str(icons[(seconds//2)%9]).zfill(2)+dn[seconds%2])
    seconds += 1

    if seconds == 240:
        get_weather()
        seconds = 0
        
        temp_text.text = str(round(data["main"]["temp"],1))+" C"
        degree_text.x = num_size(str(round(data["main"]["temp"],1)))+1
        wind_text.text = str(round(data["wind"]["speed"]))+"mph"
        high_text.text = str(round(data["main"]["temp_max"]))
        low_text.text = str(round(data["main"]["temp_min"]))
        
        temp_text.color = temp_scale[math.floor(data["main"]["temp"])+30]
        degree_text.color = temp_scale[math.floor(data["main"]["temp"])+30]
        wind_text.color = wind_scale[beaufort_scale(data["wind"]["speed"])]

        g1[0] = get_image(data[0]["weather"]["icon"])

    current_time = [str(i) for i in time.localtime(time.time())]
    date_string = current_time[2].zfill(2)+"/"+current_time[1].zfill(2)+"/"+current_time[0].zfill(4)
    time_string = current_time[3].zfill(2)+":"+current_time[4].zfill(2)+":"+current_time[5].zfill(2)

    date_text.text = date_string
    time_text.text = time_string
    
    # Draw!
    display.refresh(minimum_frames_per_second=0)

    time.sleep(0.5)
