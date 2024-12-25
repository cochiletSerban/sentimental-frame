#!/usr/bin/env python3
from PIL import Image
from inky.auto import auto
import os
import time
import threading

import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge

# move to another file

def setImage(image, saturation):
    try:
        inky.set_image(image, saturation=saturation)
    except TypeError:
        inky.set_image(image)

def strechImageToFitScreenAndDisplay(image, saturation):
    resizedimage = image.resize(inky.resolution)
    setImage(resizedimage, saturation)
    inky.show()

def keepImageOriginalAspectRationAndDisplay(image, saturation):
    image.thumbnail(inky.resolution)

    canvas = Image.new("RGB", inky.resolution, "black")
    canvas.paste(image, ((inky.resolution[0] - image.size[0]) // 2, (inky.resolution[1] - image.size[1]) // 2))

    setImage(canvas,saturation)

    inky.show()

def scaleImageToFillScreenAndDisplay(image, saturation, top_offset=0):
    """
    Scales an image to fill the screen by zooming in and cropping, maintaining aspect ratio.
    Allows vertical alignment adjustments with a top offset.

    :param image: PIL.Image object to be displayed
    :param saturation: Saturation level for the Inky display
    :param top_offset: Number of pixels to offset the image from the top (default 0)
    """
    # Calculate aspect ratios
    image_ratio = image.width / image.height
    screen_ratio = inky.resolution[0] / inky.resolution[1]

    # Determine how to scale the image
    if image_ratio > screen_ratio:
        # Image is wider than the screen; scale by height
        scale_height = inky.resolution[1]
        scale_width = int(scale_height * image_ratio)
    else:
        # Image is taller than the screen; scale by width
        scale_width = inky.resolution[0]
        scale_height = int(scale_width / image_ratio)

    # Resize the image to fill the screen dimensions (may exceed in one direction)
    scaled_image = image.resize((scale_width, scale_height), Image.ANTIALIAS)

    # Calculate the cropping box to include top_offset
    left = (scaled_image.width - inky.resolution[0]) // 2
    right = left + inky.resolution[0]

    # Apply top_offset, ensuring it stays within bounds
    top = min(max(0, top_offset), scaled_image.height - inky.resolution[1])
    bottom = top + inky.resolution[1]

    # Crop the image to fit the exact screen dimensions
    cropped_image = scaled_image.crop((left, top, right, bottom))

    # Display the cropped image
    setImage(cropped_image, saturation)
    inky.show()



    # BUTTONS = [5, 6, 16, 24]

def calculate_aspect_ratio(width, height):
    return width / height

def is_aspect_ratio_similar(image, inky_resolution, tolerance=0.3):
    image_ratio = calculate_aspect_ratio(*image.size)
    inky_ratio = calculate_aspect_ratio(*inky_resolution)
    difference = abs(image_ratio - inky_ratio) / inky_ratio
    return difference <= tolerance

def display_image(image_path):
    print(f"Displaying: {image_path}")
    image = Image.open(image_path)
    scaleImageToFillScreenAndDisplay(image,0.8)

def clear_pending_events():
    """Clears all pending GPIO events in the request queue."""
    events = request.read_edge_events()  # Read all pending events
    for event in events:
        print("Clearing event:", event.line_offset)

# #################### #


# Background thread for periodic image changes
def periodic_image_change():
    global current_image_index
    while True:
        time.sleep(60)  # 24 hours
        with lock:  # Synchronize access to current_image_index
            print("Scheduled update. Changing to the next image.")
            current_image_index = (current_image_index + 1) % len(images)
            display_image(images[current_image_index])
            clear_pending_events()

BUTTON_A_PIN = 5  # Replace with your actual GPIO pin for button A
INPUT = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)

# Find the GPIO chip and configure the button
chip = gpiodevice.find_chip_by_platform()
line_config = {BUTTON_A_PIN: INPUT}
request = chip.request_lines(consumer="inky7-buttons", config=line_config)

inky = auto()
saturation = 0.8
current_image_index = 0
lock = threading.Lock()  # To synchronize access to current_image_index

image_dir = 'images'

images = [
    os.path.join(image_dir, f)
    for f in os.listdir(image_dir)
    if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))
]



# Main event handling logic
def main_event_loop():
    global current_image_index
    while True:
        for event in request.read_edge_events():
            if event.line_offset == BUTTON_A_PIN:  # Ensure it's the correct button
                with lock:  # Synchronize access to current_image_index
                    print("Button pressed. Updating display...")
                    current_image_index = (current_image_index + 1) % len(images)
                    display_image(images[current_image_index])
                    clear_pending_events()
   
# Start the background thread
thread = threading.Thread(target=periodic_image_change, daemon=True)
thread.start()

main_event_loop()