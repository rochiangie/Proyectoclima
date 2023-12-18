import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk, messagebox
from app_clima import ClimaApp

class TestClimaApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = ClimaApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('app_clima.requests.get')  
    @patch('app_clima.ClimaApp.obtener_imagen_desde_url')
    def test_obtener_clima_exitoso(self, mock_obtener_imagen, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'main': {'temp': 300},
            'weather': [{'description': 'sunny', 'icon': '01d'}]
        }
        mock_get.return_value = mock_response

        self.app.ciudad_entry.insert(0, 'CiudadEjemplo')

        # Mock para la imagen
        #mock_imagen = MagicMock()
        #mock_obtener_imagen.return_value = mock_imagen

        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()

            mock_mostrar_mensaje.assert_called_with('Clima', 'Temperatura: 26.85°C\nDescripción: Sunny')
            mock_obtener_imagen.assert_called_with('http://openweathermap.org/img/w/01d.png')

            # Verificar que la imagen se configure correctamente en el Label
            #self.assertEqual(self.app.imagen, mock_imagen)
            #self.app.imagen_label.configure.assert_called_with(image=mock_imagen)

    def test_obtener_clima_error_ciudad_vacia(self):
        # Prueba cuando no se ingresa una ciudad
        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()
            mock_mostrar_mensaje.assert_called_with('Error', 'Ingresa el nombre de la ciudad')

    @patch('app_clima.requests.get', side_effect=Exception('Error simulado'))
    def test_obtener_clima_error_request(self, mock_get):
        # Prueba cuando la solicitud a la API devuelve un error
        self.app.ciudad_entry.insert(0, 'CiudadEjemplo')

        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()
            mock_mostrar_mensaje.assert_called_with('Error', 'Error al obtener el clima: Error simulado')

if __name__ == '__main__':
    unittest.main()


