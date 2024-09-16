import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class pypicsum:
    def __init__(self, image_x, image_y=None, label=None):
        self.image_x = image_x
        self.image_y = image_y
        self.label = label

        self.load_image()

    def load_image(self):
        # URL of the placeholder image from Lorem Picsum
        if self.image_y != None:
            url = f"https://picsum.photos/{self.image_x}/{self.image_y}"
        else:
            url = f"https://picsum.photos/{self.image_x}"

        # Send a request to get the image
        response = requests.get(url)

        # Convert the image content to a format that PIL can open
        img_data = BytesIO(response.content)

        # Open the image with PIL
        img = Image.open(img_data)

        # Convert the image to a format Tkinter can display
        img_tk = ImageTk.PhotoImage(img)

        # Display the image in the label
        self.label.configure(image=img_tk)
        self.label.image = img_tk  # keep a reference to the image
