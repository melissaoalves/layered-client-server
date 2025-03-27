import tkinter as tk
from tkinter import filedialog, Label, Button
import requests
from PIL import ImageTk, Image
import io

SERVER_URL = 'http://localhost:5000/upload'

def send_image():
    path = filedialog.askopenfilename()
    if not path:
        return

    with open(path, 'rb') as img_file:
        response = requests.post(SERVER_URL, files={'image': img_file})

    data = response.json()
    show_image_from_url(data['original'], original_label)
    show_image_from_url(data['processed'], processed_label)

def show_image_from_url(url, label):
    response = requests.get(f"http://localhost:5000{url}")
    img = Image.open(io.BytesIO(response.content)).resize((300, 300))
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

app = tk.Tk()
app.title("Cliente de Imagem")
app.geometry("700x500")
app.configure(bg="#f8f8f8")

button = Button(app, text="Enviar Imagem", command=send_image, font=("Arial", 12), width=20)
button.pack(pady=20)

label_frame = tk.Frame(app, bg="#f8f8f8")
label_frame.pack()

Label(label_frame, text="Imagem Original", font=("Arial", 12), bg="#f8f8f8").grid(row=0, column=0, padx=40)
Label(label_frame, text="Imagem Processada", font=("Arial", 12), bg="#f8f8f8").grid(row=0, column=1, padx=40)

image_frame = tk.Frame(app, bg="#f8f8f8")
image_frame.pack(pady=10)

original_label = Label(image_frame, bg="white", width=300, height=300)
original_label.grid(row=0, column=0, padx=20)

processed_label = Label(image_frame, bg="white", width=300, height=300)
processed_label.grid(row=0, column=1, padx=20)

app.mainloop()
