import os
from PIL import Image

def resize_and_rotate_images(target_width=800):
    # Get the current working directory
    current_dir = os.getcwd()

    # Supported image formats
    supported_formats = (".png", ".jpg", ".jpeg", ".webp")

    # Process each file in the directory
    for file_name in os.listdir(current_dir):
        if file_name.lower().endswith(supported_formats):
            file_path = os.path.join(current_dir, file_name)

            try:
                # Open the image
                with Image.open(file_path) as img:
                    # Check if the image is portrait (height > width)
                    if img.height > img.width:
                        img = img.rotate(90, expand=True)  # Rotate 90 degrees to landscape
                        print(f"Rotated {file_name} to landscape")

                    # Get original dimensions
                    original_width, original_height = img.size

                    # Calculate new dimensions while maintaining aspect ratio
                    aspect_ratio = original_height / original_width
                    target_height = int(target_width * aspect_ratio)

                    # Resize the image
                    resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                    # Save the resized image (overwrite the original)
                    resized_img.save(file_path)

                    print(f"Resized {file_name} to {target_width}x{target_height}")

            except Exception as e:
                print(f"Failed to process {file_name}: {e}")


if __name__ == "__main__":
    resize_and_rotate_images(target_width=800)
