#!/usr/bin/env python3
from PIL import Image
from inky.auto import auto
import os
import time

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

def scaleImageToFillScreenAndDisplay(image, saturation):
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

    # Calculate the cropping box to center the image
    left = (scaled_image.width - inky.resolution[0]) // 2
    top = (scaled_image.height - inky.resolution[1]) // 2
    right = left + inky.resolution[0]
    bottom = top + inky.resolution[1]

    # Crop the image to fit the exact screen dimensions
    cropped_image = scaled_image.crop((left, top, right, bottom))

    # Display the cropped image
    setImage(cropped_image, saturation)
    inky.show()

def calculate_aspect_ratio(width, height):
    return width / height

def is_aspect_ratio_similar(image, inky_resolution, tolerance=0.3):
    image_ratio = calculate_aspect_ratio(*image.size)
    inky_ratio = calculate_aspect_ratio(*inky_resolution)
    difference = abs(image_ratio - inky_ratio) / inky_ratio
    return difference <= tolerance

# #################### #

def loopAllImages(images):
    for image_path in images:
        image = Image.open(image_path)

        if is_aspect_ratio_similar(image, inky.resolution, tolerance=0.3):
            strechImageToFitScreenAndDisplay(image, saturation)
        else:
            keepImageOriginalAspectRationAndDisplay(image, saturation)

        time.sleep(60)

inky = auto()
saturation = 0.8

image_dir = 'images'

images = [
    os.path.join(image_dir, f)
    for f in os.listdir(image_dir)
    if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))
]

print(images)



scaleImageToFillScreenAndDisplay(Image.open(images[2]), saturation)