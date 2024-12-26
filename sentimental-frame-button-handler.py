#!/usr/bin/env python3
import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge


import subprocess

# used to prevent trigger another image change while one is in progress
def clear_pending_events():
    """Clears all pending GPIO events in the request queue."""
    events = request.read_edge_events() 
    for event in events:
        print("Clearing event:", event.line_offset)


# GPIO pin setup an button config
BUTTON_A_PIN = 5  
BUTTON_B_PIN = 6

INPUT = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)
chip = gpiodevice.find_chip_by_platform()
line_config = {BUTTON_A_PIN: INPUT, BUTTON_B_PIN: INPUT}
request = chip.request_lines(consumer="inky7-buttons", config=line_config)


def main_event_loop():
    while True: # sometimes needed to keep the program runnig
        for event in request.read_edge_events():
            if event.line_offset == BUTTON_A_PIN or event.line_offset == BUTTON_B_PIN:  # Ensure it's the correct button
                direction = "up" if event.line_offset == BUTTON_A_PIN else "down"
                subprocess.run(["python3", "sentimental-frame-next-image.py", direction], capture_output=True, text=True)
                clear_pending_events()
   

main_event_loop()
