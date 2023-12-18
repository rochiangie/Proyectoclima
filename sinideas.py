import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk

class ClimaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clima App")

        # Crear un estilo
        self.style = ttk.Style()

        # Cambiar el tema (puedes elegir 'clam', 'alt', 'default', etc.)
        self.style.theme_use('alt')

        # Configurar estilo para etiquetas y botones
        self.style.configure('TLabel', font=('Arial', 12), foreground='black')
        self.style.configure('TButton', font=('Arial', 12), foreground='blue')

        print("Bienvenido a la aplicación del clima")

        self.ciudad_label = ttk.Label(root, text="Nombre de la ciudad:")
        self.ciudad_label.pack()

        self.ciudad_entry = ttk.Entry(root)
        self.ciudad_entry.pack()

        self.buscar_button = ttk.Button(root, text="Buscar clima", command=self.obtener_clima)
        self.buscar_button.pack()

        self.imagen_label = ttk.Label(root)
        self.imagen_label.pack()

    def obtener_clima(self):
        ciudad = self.ciudad_entry.get()
        if ciudad:
            try:
                api_key = "8aa90031f4073ef8a1f233dd279c05d4"  # Reemplaza con tu clave de OpenWeatherMap
                url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}"
                response = requests.get(url)
                data = response.json()

                temperatura_kelvin = data['main']['temp']
                temperatura_celsius = temperatura_kelvin - 273.15

                descripcion = data['weather'][0]['description']

                mensaje = f"Temperatura: {temperatura_celsius:.2f}°C\nDescripción: {descripcion.capitalize()}"

                self.mostrar_mensaje("Clima", mensaje)

                # Mostrar la imagen correspondiente al clima
                icono = data['weather'][0]['icon']
                imagen_url = f"http://openweathermap.org/img/w/{icono}.png"
                imagen = self.obtener_imagen_desde_url(imagen_url)
                self.mostrar_imagen(imagen)

            except Exception as e:
                self.mostrar_mensaje("Error", f"Error al obtener el clima: {e}")
        else:
            self.mostrar_mensaje("Error", "Ingresa el nombre de la ciudad")

    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def obtener_imagen_desde_url(self, url):
        response = requests.get(url, stream=True)
        imagen = Image.open(response.raw)
        imagen = ImageTk.PhotoImage(imagen)
        return imagen

    def mostrar_imagen(self, imagen):
        self.imagen_label.configure(image=imagen)
        self.imagen_label.image = imagen

if __name__ == "__main__":
    root = tk.Tk()
    app = ClimaApp(root)
    root.mainloop()
