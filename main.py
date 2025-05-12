import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

root = tk.Tk()

root.title("WaterMarker")
root.geometry("1000x1000")

#Object containing image to watermark (copy)
img_to_mark = None
marked_img = None
watermark_img = None

# Image upload function
def img_upload():
    global image_label
    global img_to_mark
    file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*")))
    if file_path:
        try:
            original_img = Image.open(file_path)
            img_to_mark = original_img.copy()

            display_thumb = original_img.copy()
            display_thumb.thumbnail((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(display_thumb)

            image_label.config(image=tk_image)
            image_label.image = tk_image
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text=f"Error loading image: {e}", image='')
            img_to_mark = None
    else:
        return None
# Watermark upload
def watermark_upload():
    global watermark_label
    global watermark_img
    file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*")))
    if file_path:
        try:
            original_watermark = Image.open(file_path)
            watermark_img = original_watermark.copy()

            display_thumb = original_watermark.copy()
            display_thumb.thumbnail((200, 200), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(display_thumb)

            watermark_label.config(image=tk_image)
            watermark_label.image = tk_image

        except Exception as e:
            print(f"Error loading image: {e}")
            watermark_label.config(text=f"Error loading image: {e}", image='')
            watermark_img = None
    else:
        return None

# Apply image watermark function
def image_mark():
    global watermark_img
    global img_to_mark
    global marked_img
    global marked_image_label

    if not img_to_mark:
        messagebox.showerror("Error", "Please upload an image to watermark first.")
        return
    if not watermark_img:
        messagebox.showerror("Error", "Please upload watermark first")
        return
    # Create copies of images to work with
    img_to_process = img_to_mark.copy()
    watermark_to_apply = watermark_img.copy()

    main_w, main_h = img_to_process.size
    wm_w, wm_h = watermark_to_apply.size

    # Watermark resizing
    target_wm_width = main_w // 5
    if target_wm_width < 1:
        target_wm_width = 1
    if watermark_to_apply.width > target_wm_width:
        aspect_ratio = watermark_to_apply.height / watermark_to_apply.width
        target_wm_height = int(target_wm_width * aspect_ratio)
        if target_wm_height < 1:
            target_wm_height = 1
        watermark_to_apply = watermark_to_apply.resize((target_wm_height, target_wm_width), Image.Resampling.LANCZOS)
        wm_h, wm_w = watermark_to_apply.size

    # Pasting Logic
    padding = main_w // 50
    position_x = main_w - wm_w - padding
    position_y = main_h - wm_h - padding

    if position_y < 0:
        position_y = 0
    if position_x < 0:
        position_x = 0

#     Transparency if PNG files with alpha channel
    if watermark_to_apply.mode == "RGBA":
        transparent_layer = Image.new('RGBA', img_to_process.size, (0,0,0,0))
        transparent_layer.paste(watermark_to_apply, (position_x, position_y))
        img_to_process = Image.alpha_composite(img_to_process.convert('RGBA'), transparent_layer)
    else:
        if img_to_process.mode == "RGBA":
            img_to_process = img_to_process.convert('RGB')
        img_to_process.paste(watermark_to_apply, (position_x,position_y))

    display_thumb = img_to_process.copy()
    display_thumb.thumbnail((200, 200), Image.Resampling.LANCZOS)
    tk_image_mark = ImageTk.PhotoImage(display_thumb)
    marked_image_label.config(image=tk_image_mark)
    marked_image_label.image = tk_image_mark
    marked_img = img_to_process

# Text watermark function
def text_mark():
    global img_to_mark
    global marked_image_label
    global marked_img
    img_to_process = img_to_mark.copy()
    if img_to_process.mode != 'RGBA':
        img_to_process = img_to_process.convert('RGBA')
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
    font = ImageFont.load_default(int(font_size/6))
    draw.text((x,y), text, fill=(255,255,255,128), font=font, anchor='ms')
    img_to_process.thumbnail((200, 200), Image.Resampling.LANCZOS)
    tk_image_mark = ImageTk.PhotoImage(img_to_process)
    marked_image_label.config(image=tk_image_mark)
    marked_image_label.image = tk_image_mark
    marked_img = img_to_process

# Save image function
def save_img():
    global marked_img
    if marked_img:
        filetypes = [("PNG files", "*.png"),
                     ("JPEG files", "*.jpg"),
                     ("All files", "*.*")]
        save_path = filedialog.asksaveasfilename(filetypes=filetypes,
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
greeting_label.grid(row=0, column=1, pady=10)

image_label = tk.Label(root)
image_label.grid(row=1, column=1, pady=5)

upload_button = tk.Button(root, text="Upload Image to watermark", command=img_upload)
upload_button.grid(row=2, column=1, pady=5)

txt_label = tk.Label(root, text="Provide text to watermark image:")
txt_label.grid(row=3, column=0, pady=10, padx=5)
text_to_mark = tk.Text(root, height=1, width=25, bg="white")
text_to_mark.grid(row=4, column=0, pady=5, padx=5)

mark_with_text = tk.Button(root, text="Watermark image with text", command=text_mark)
mark_with_text.grid(row=5, column=0, pady=5, padx=5)

mark_with_image = tk.Label(root, text="or watermark with another image(logo)")
mark_with_image.grid(row=3, column=2, pady=10)

watermark_label = tk.Label(root)
watermark_label.grid(row=4, column=2, pady=5)

upload_mark_button = tk.Button(root, text="Upload watermark image or logo", command=watermark_upload)
upload_mark_button.grid(row=5, column=2, pady=5)

marked_image_label = tk.Label(root)
marked_image_label.grid(row=4, column=1, pady=5)

apply_button = tk.Button(root, text="Apply image or logo watermark", command=image_mark)
apply_button.grid(row=6, column=1)

save_button = tk.Button(root, text="Save", command=save_img)
save_button.grid(row=7, column=1, sticky=tk.E)
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=7, column=1, sticky=tk.W)

# Configure column weights for resizing behavior if desired
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1) # Central column for options might not need to expand as much
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1) # Allow row with images to expand
root.mainloop()