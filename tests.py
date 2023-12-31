import unittest
from unittest import TestCase
from unittest.mock import patch
from tkinter import Tk
from app_clima import ClimaApp

class TestClimaApp(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = ClimaApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('app_clima.requests.get')  
    def test_obtener_clima_exitoso(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            'main': {'temp': 300},
            'weather': [{'description': 'sunny', 'icon': '01d'}]
        }

        self.app.ciudad_entry.insert(0, 'CiudadEjemplo')

        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()

            mock_mostrar_mensaje.assert_called_with('Clima', 'Temperatura: 26.85°C\nDescripción: Sunny')
            self.assertIsNotNone(self.app.imagen)

    def test_obtener_clima_error_ciudad_vacia(self):
        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()

            mock_mostrar_mensaje.assert_called_with('Error', 'Ingresa el nombre de la ciudad')
            self.assertIsNone(self.app.imagen_label.image)

    @patch('app_clima.requests.get', side_effect=Exception('Error de red'))
    def test_obtener_clima_error_request(self, mock_get):
        self.app.ciudad_entry.insert(0, 'CiudadError')

        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()

            mock_mostrar_mensaje.assert_called_with('Error', 'Error al obtener el clima: Error de red')
            self.assertIsNone(self.app.imagen_label.image)

if __name__ == '__main__':
    unittest.main()
