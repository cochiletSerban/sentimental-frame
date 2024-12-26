from PIL import Image



def setImage(image, saturation, inky):
    try:
        inky.set_image(image, saturation=saturation)
    except TypeError:
        inky.set_image(image)

def strechImageToFitScreenAndDisplay(image, saturation):
    global inky
    resizedimage = image.resize(inky.resolution)
    setImage(resizedimage, saturation)
    inky.show()

def keepImageOriginalAspectRationAndDisplay(image, saturation):
    global inky
    image.thumbnail(inky.resolution)

    canvas = Image.new("RGB", inky.resolution, "black")
    canvas.paste(image, ((inky.resolution[0] - image.size[0]) // 2, (inky.resolution[1] - image.size[1]) // 2))

    setImage(canvas,saturation)

    inky.show()

def scaleImageToFillScreenAndDisplay(image, saturation, inky, top_offset=0):
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
    setImage(cropped_image, saturation, inky)
    inky.show()



    # BUTTONS = [5, 6, 16, 24]

def calculate_aspect_ratio(width, height):
    return width / height

def is_aspect_ratio_similar(image, inky_resolution, tolerance=0.3):
    image_ratio = calculate_aspect_ratio(*image.size)
    inky_ratio = calculate_aspect_ratio(*inky_resolution)
    difference = abs(image_ratio - inky_ratio) / inky_ratio
    return difference <= tolerance

def display_image(image_path, inky):
    print(f"Displaying: {image_path}")
    image = Image.open(image_path)
    scaleImageToFillScreenAndDisplay(image, 0.8, inky)
