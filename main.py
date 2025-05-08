import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


root = tk.Tk()

root.title("WaterMarker Application")
root.geometry("1000x750")


# ----TK UI----
greeting_label = tk.Label(root, text='Welcome to WaterMarker\n\n'
                                     'Your uploaded image and watermark will display below\n'
                                     'Your final image will be displayed at the bottom for saving')
greeting_label.pack(side=tk.TOP, pady=10)

image_label = tk.Label(root)
image_label.pack(side=tk.TOP, pady=20)

# Image upload function
def img_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(img)
            image_label.config(image=tk_image)
            image_label.image = tk_image
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text=f"Error loading image: {e}", image='')

upload_button = tk.Button(root, text="Upload Image to watermark", command=img_upload)
upload_button.pack(side=tk.TOP, pady=20)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(side=tk.BOTTOM, pady=10)
root.mainloop()