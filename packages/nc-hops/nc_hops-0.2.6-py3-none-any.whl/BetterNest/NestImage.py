from PIL import Image, ImageDraw, ImageChops
from typing import Union
import os


def trim_whitespace(image: Image) -> Image:
    """
    Trims the white border from an image

    :param image: PIL Image object
    :return: Cropped PIL Image object
    """
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)


def draw_on_lbl(
        file: str,
        coordinates: list,
        length: Union[float, int],
        width: Union[float, int]) -> tuple:
    """
    A function to modify the hops .jpeg file
    It cuts off the white part of the image
    Takes in the parameter of the board and finds the center of each part inside the nestboard
    For now it just draws a circle on the center of each part
    :param file: File path
    :param coordinates: List containing coordinates
    :param length: Length of the board
    :param width: Width of the board
    :return: Returns a tuple with the new file name, and the new image size dimensions
    """

    # Load the image from the provided path
    image = Image.open(file)

    # Trim the whitespace
    trimmed_image = trim_whitespace(image)
    trimmed_image.save('trimmed_board_image.jpg')  # Temporary save the trimmed image

    # Get the new size of the image after trimming
    new_width, new_height = trimmed_image.size

    # Create a draw object
    draw = ImageDraw.Draw(trimmed_image)
    radius = 10  # radius of the circle

    # Scale factors for x and y coordinates
    scale_factor_x = new_width / length  # Scale for X based on the trimmed image width and real width in mm
    scale_factor_y = new_height / width  # Scale for Y based on the trimmed image height and real height in mm

    scaled_coordinates = []
    for (x_mm, y_mm, board_id) in coordinates:
        # Convert from mm to pixels using the scale factors
        x_px = x_mm * scale_factor_x
        y_px = new_height - (y_mm * scale_factor_y)  # Invert the Y coordinate to match image coordinate system

        # Define the bounding box of the circle
        left_up_point = (x_px - radius, y_px - radius)
        right_down_point = (x_px + radius, y_px + radius)

        scaled_coordinates.append((x_px, y_px, board_id))
        # Draw the circle on the image
        draw.ellipse([left_up_point, right_down_point], outline="blue", width=2)

    # Save the modified image with a suffix
    output_path = os.path.join(os.path.dirname(__file__), file.split('/')[-1].split('.')[0] + '_resized.jpg')
    trimmed_image.save(output_path)
    os.remove('trimmed_board_image.jpg')  # Remove the trimmed board
    return output_path, new_width, new_height, scaled_coordinates

