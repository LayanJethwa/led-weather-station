import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time

# Release old displays
displayio.release_displays()

# Crete led matrix
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Groups

while True:
    group_root = displayio.Group()
    group_text = displayio.Group()

    current_time = [str(i) for i in time.localtime(time.time())]
    date = current_time[2].zfill(2)+"/"+current_time[1].zfill(2)+"/"+current_time[0].zfill(4)
    hours = current_time[3].zfill(2)+":"+current_time[4].zfill(2)+":"+current_time[5].zfill(2)
    
    # Text element Text-0
    text_0 = adafruit_display_text.label.Label(
         terminalio.FONT,
        color=0xff0000,
        text = date)
    text_0.x = 2
    text_0.y = 6
    group_text.append(text_0)

    text_1 = adafruit_display_text.label.Label(
         terminalio.FONT,
        color=0xff0000,
        text = hours)
    text_1.x = 2
    text_1.y = 18
    group_text.append(text_1)
    
    # Add groups
    group_root.append(group_text)
    display.root_group = group_root
    
    # Draw!
    display.refresh(minimum_frames_per_second=0)
