#!/usr/bin/env python3

import os
import time
from PIL import Image
from inky.auto import auto
import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge

# Initialize Inky display
inky = auto()
saturation = 0.8

# GPIO setup for button A
BUTTON_A_PIN = 5  # Replace with your actual GPIO pin for button A
INPUT = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)

# Find the GPIO chip and configure the button
chip = gpiodevice.find_chip_by_platform()
line_config = {BUTTON_A_PIN: INPUT}
request = chip.request_lines(consumer="inky7-buttons", config=line_config)

# Function to keep image aspect ratio and display it
def keepImageOriginalAspectRationAndDisplay(image, saturation):
    image.thumbnail(inky.resolution)
    canvas = Image.new("RGB", inky.resolution, "black")
    canvas.paste(image, ((inky.resolution[0] - image.size[0]) // 2, (inky.resolution[1] - image.size[1]) // 2))
    inky.set_image(canvas, saturation=saturation)
    inky.show()

# Function to scale image to fill the screen
def scaleImageToFillScreenAndDisplay(image, saturation):
    image_ratio = image.width / image.height
    screen_ratio = inky.resolution[0] / inky.resolution[1]

    if image_ratio > screen_ratio:
        scale_height = inky.resolution[1]
        scale_width = int(scale_height * image_ratio)
    else:
        scale_width = inky.resolution[0]
        scale_height = int(scale_width / image_ratio)

    scaled_image = image.resize((scale_width, scale_height), Image.ANTIALIAS)
    left = (scaled_image.width - inky.resolution[0]) // 2
    top = (scaled_image.height - inky.resolution[1]) // 2
    cropped_image = scaled_image.crop((left, top, left + inky.resolution[0], top + inky.resolution[1]))
    inky.set_image(cropped_image, saturation=saturation)
    inky.show()

# Get all images in the /images directory
image_dir = 'images'
images = [
    os.path.join(image_dir, f)
    for f in os.listdir(image_dir)
    if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))
]

# Ensure there are images to display
if not images:
    print("No images found in the /images directory.")
    exit(1)

# Function to handle button press
def handle_button(event):
    global current_image_index
    current_image_index = (current_image_index + 1) % len(images)  # Move to the next image
    display_image(images[current_image_index])

# Display the image based on aspect ratio similarity
def display_image(image_path):
    image = Image.open(image_path)
    image_ratio = image.width / image.height
    screen_ratio = inky.resolution[0] / inky.resolution[1]
    tolerance = 0.3  # 30% tolerance for aspect ratio similarity

    if abs(image_ratio - screen_ratio) / screen_ratio <= tolerance:
        keepImageOriginalAspectRationAndDisplay(image, saturation)
    else:
        scaleImageToFillScreenAndDisplay(image, saturation)

# Main loop
current_image_index = 0
display_image(images[current_image_index])  # Display the first image

start_time = time.time()
while True:
    # Check for button press
    for event in request.read_edge_events():
        handle_button(event)

    # Change image every 5 minutes
    if time.time() - start_time >= 300:  # 300 seconds = 5 minutes
        current_image_index = (current_image_index + 1) % len(images)
        display_image(images[current_image_index])
        start_time = time.time()
