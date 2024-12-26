#!/usr/bin/env python3
from PIL import Image
from inky.auto import auto
import os
import argparse
import image_methods as Frame
import index_methods as Current_Index


parser = argparse.ArgumentParser(description="Increment or decrement image index.")
parser.add_argument("direction", choices=["up", "down"], help="Direction to adjust the image index")
args = parser.parse_args()


inky = auto()
image_dir = 'images'

images = sorted(
    [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))
    ],
    key=lambda x: os.path.getctime(x)
)

index = Current_Index.load_index()

if args.direction == "up":
    index += 1
elif args.direction == "down":
    index -= 1

if index >= len(images):
    index = 0
elif index < 0:
    index = len(images) - 1

Current_Index.save_index(index)

Frame.display_image(images[index], inky)
