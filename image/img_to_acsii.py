import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    return image.resize((new_width, int(new_width * ratio)))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = list(image.getdata())
    return ''.join(ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255] for pixel in pixels)


def convert_image_to_ascii(path, new_width=100):
    try:
        image = Image.open(path)
        image = resize_image(image, new_width)
        image = grayify(image)  # Ensure it's grayscale
        pixels = list(image.getdata())  # Convert pixel data to list of ints (0–255)
        ascii_str = ''.join(ASCII_CHARS[pixel // 25] for pixel in pixels)
        ascii_image = "\n".join(
            ascii_str[i:(i + new_width)] for i in range(0, len(ascii_str), new_width)
        )
        return ascii_image
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e}")
        return None


def open_file():
    filepath = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")]
    )
    if filepath:
        ascii_art = convert_image_to_ascii(filepath, new_width=100)
        if ascii_art:
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, ascii_art)

# GUI Setup
root = tk.Tk()
root.title("Image to ASCII Art")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_upload = tk.Button(frame, text="📂 Upload Image", command=open_file)
btn_upload.pack()

text_output = scrolledtext.ScrolledText(root, font=("Courier", 6), wrap=tk.WORD, bg="black", fg="white")
text_output.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()
