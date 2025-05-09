import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

root = tk.Tk()

root.title("WaterMarker")
root.geometry("500x750")

#Object containing image to watermark (copy)
img_to_mark = None
marked_img = None

# Image upload function
def img_upload():
    global image_label
    global img_to_mark
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(img)
            image_label.config(image=tk_image)
            image_label.image = tk_image
            img_to_mark = img.copy()
            return img_to_mark
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text=f"Error loading image: {e}", image='')
            return None
    else:
        return None

# Text watermark function
def text_mark():
    global img_to_mark
    global marked_image_label
    global marked_img
    img_to_process = img_to_mark.copy()
    draw = ImageDraw.Draw(img_to_process)
    text = text_to_mark.get("1.0", tk.END)
    w, h = img_to_process.size
    x, y = int(round(w/2)), int(round(h/2))
    if x > y:
        font_size = y
    elif y > x:
        font_size = x
    else:
        font_size = x
    font = ImageFont.truetype("Arial.ttf", int(font_size/6))
    draw.text((x,y), text, fill=(255,255,255,128), font=font, anchor='ms')
    img_to_process.thumbnail((200, 200), Image.Resampling.LANCZOS)
    tk_image_mark = ImageTk.PhotoImage(img_to_process)
    marked_image_label.config(image=tk_image_mark)
    marked_image_label.image = tk_image_mark
    marked_img = img_to_process

def logo_upload():
    global image_label
    global img_to_mark
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(img)
            image_label.config(image=tk_image)
            image_label.image = tk_image
            img_to_mark = img.copy()
            return img_to_mark
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text=f"Error loading image: {e}", image='')
            return None
    else:
        return None

# Save image function
def save_img():
    global marked_img
    if marked_img:
        filetypes = [("PNG files", "*.png"),
                     ("JPEG files", "*.jpg"),
                     ("All files", "*.*")]
        save_path = filedialog.asksaveasfile(filetypes=filetypes,
                                             defaultextension=".png",
                                             title="Save watermarked image as..")
        if save_path:
            try:
                marked_img.save(save_path)
                messagebox.showinfo("Image Saved", f"Watermarked image saved to:\n{save_path}")
                print(f"DEBUG: Image saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save image: {e}")
                print(f"DEBUG: Error saving image: {e}")
    else:
        messagebox.showwarning("Nothing to Save",
                               "No watermarked image available to save. Please apply a watermark first.")
        print("DEBUG: Save attempt but marked_img is None.")


# ----TK UI----
greeting_label = tk.Label(root, text='Welcome to WaterMarker\n\n'
                                     'Your uploaded image and watermark will display below\n'
                                     'Images can be watermarked with text or logos\n'
                                     'Your final image will be displayed at the bottom for saving')
greeting_label.pack(side=tk.TOP, pady=10)

image_label = tk.Label(root)
image_label.pack(side=tk.TOP, pady=5)

upload_button = tk.Button(root, text="Upload Image to watermark", command=img_upload)
upload_button.pack(side=tk.TOP, pady=5)

txt_label = tk.Label(root, text="Provide text to watermark image:")
txt_label.pack(side=tk.TOP, pady=10)
text_to_mark = tk.Text(root, height=1, width=25, bg="white")
text_to_mark.pack(side=tk.TOP, pady=5)

mark_with_text = tk.Button(root, text="Watermark image with text", command=text_mark)
mark_with_text.pack(side=tk.TOP, pady=5)

mark_with_image = tk.Label(root, text="or watermark with another image(logo)")
mark_with_image.pack(side=tk.TOP, pady=10)
upload_mark_button = tk.Button(root, text="Upload watermark image or logo", command=img_upload)
upload_mark_button.pack(side=tk.TOP, pady=5)

marked_image_label = tk.Label(root)
marked_image_label.pack(side=tk.TOP)

save_button = tk.Button(root, text="Save", command=save_img)
save_button.pack(side=tk.TOP, pady=5)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(side=tk.TOP, pady=5)
root.mainloop()