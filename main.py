import tkinter as tk
from io import BytesIO
from tkinter import filedialog, messagebox

import cv2
import numpy as np
import requests
from PIL import Image, ImageTk


def convert_to_gray_api(img):
    API_ENDPOINT = "https://0txn2cwcf7.execute-api.ap-south-1.amazonaws.com/dev"

    is_success, im_buf_arr = cv2.imencode(".png", img)
    byte_im = im_buf_arr.tobytes()

    r = requests.post(url=API_ENDPOINT, data=byte_im)

    img_ = Image.open(BytesIO(r.content))

    return np.asarray(img_)

def process_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        try:
            img = cv2.imread(file_path)
            img_gray = convert_to_gray_api(img)

            # Display original image
            original_img = Image.open(file_path)
            original_img.thumbnail((600, 600))
            original_photo = ImageTk.PhotoImage(original_img)
            original_label.config(image=original_photo)
            original_label.image = original_photo

            # Display processed image
            processed_img = Image.fromarray(img_gray)
            processed_img.thumbnail((600, 600))
            processed_photo = ImageTk.PhotoImage(processed_img)
            processed_label.config(image=processed_photo)
            processed_label.image = processed_photo

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Image Processing")
root.configure(bg="#007bff")  # Set background color to blue

# Increase initial screen size
root.geometry("800x650")

# Create a navbar
navbar = tk.Frame(root, bg="#335")
navbar.pack(fill="x")

title_label = tk.Label(navbar, text="Serverless Image Processing Using AWS Lambda", fg="white", bg="#333", font=("Arial", 16))
title_label.pack(pady=10)

# Create a frame to hold the buttons and labels
frame = tk.Frame(root, padx=25, pady=15, bg="#007bff")
frame.pack()

# Button to select and process the image
process_button = tk.Button(frame, text="Select and Process Image", command=process_image, bg="#FFFFFF", fg="#007bff", font=("Arial", 12))
process_button.grid(row=0, column=0, columnspan=2, pady=10)

# Center the button
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Label to display the original image
original_label = tk.Label(frame, bg="#CCCCCC")  # Set background color to white
original_label.grid(row=1, column=0, padx=10)

# Label to display the processed image
processed_label = tk.Label(frame, bg="#FFFFFF")  # Set background color to white
processed_label.grid(row=1, column=1, padx=10)

# Create a footer
footer = tk.Frame(root, bg="#333", pady=10)
footer.pack(fill="x", side="bottom")

footer_text = tk.Label(footer, text="© 2024 Image Processing App. All rights reserved.", fg="white", bg="#333", font=("Arial", 10))
footer_text.pack()

# Centering the window
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Run the Tkinter event loop
root.mainloop()
