from PIL import Image

def mostrar_imagen_en_consola(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen)

        # Obtener dimensiones de la imagen
        ancho, alto = imagen.size

        # Redimensionar la imagen si es muy grande para la consola
        if ancho > 80 or alto > 40:
            imagen = imagen.resize((80, 40))

        # Mostrar cada píxel de la imagen en la consola
        for y in range(imagen.height):
            fila = ""
            for x in range(imagen.width):
                # Obtener el valor de intensidad de grises (0 a 255) del píxel
                intensidad_gris = sum(imagen.getpixel((x, y))) / 3
                # Convertir la intensidad a un carácter ASCII
                caracter_ascii = " .:-=+*%#@"[int(intensidad_gris / 25.5)]
                fila += caracter_ascii
            print(fila)
    except Exception as e:
        print(f"Error al mostrar la imagen: {e}")

# Ruta de la imagen a mostrar
ruta_imagen = "ejemplo.jpg"  # Cambia por la ruta de tu imagen

# Mostrar la imagen en la consola
mostrar_imagen_en_consola(ruta_imagen)
