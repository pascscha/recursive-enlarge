#!/usr/bin/python3

from PIL import Image
import sys
import os


def recursive_enlarge(path, resize_factor, file_endings=[".gif", ".png", ".bmp", ".jpg"], resample=Image.NEAREST):
    """
    Recursively enlarges Images in the given folder and all subfolders.

    :param path The start filepath
    :param resize_factor The factor by which the images get resized
    :param file_endings The file endings for images we want to resize
    :param resample The PIL resampling method
    """

    # Iterate through every element (file or folder) in our filepath
    for element in os.listdir(path):
        # Construct the full path of the element (os.listdir only produces filenames not the full path)
        element_path = os.path.join(path, element)

        # Check wether our element is a folder, if yes we recursively call our function on that folder
        if os.path.isdir(element_path):
            recursive_enlarge(element_path, resize_factor, file_endings=file_endings, resample=resample)

        # If the file is not a folder, we check wether its one of our images
        elif element[-4:].lower() in file_endings:

            # create backup if it does not exist yet
            if not os.path.exists(element_path + ".bak"):
                image = Image.open(element_path)  # Open Image
                os.rename(element_path, element_path + ".bak")  # Create backup of image

            # If the backup already exits we open the backup as our basis for modifying the file.
            else:
                image = Image.open(element_path + ".bak")

            # Calculate the dimensions of the new image
            old_size = image.size
            new_size = (int(old_size[0] * resize_factor), int(old_size[1] * resize_factor))

            # Resize and save the image
            image = image.resize(new_size, resample=resample)
            image.save(element_path)


if __name__ == "__main__":
    # Get the path and resize factor from the system arguments
    path = sys.argv[1]
    resize_factor = float(sys.argv[2])

    # Run our recursive function
    recursive_enlarge(path, resize_factor)
