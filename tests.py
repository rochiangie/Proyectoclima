import unittest
from unittest.mock import patch
from tkinter import Tk
from app_clima import ClimaApp

class TestClimaApp(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = ClimaApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('app_clima.requests.get')  # Mockear la llamada a requests.get
    def test_obtener_clima_exitoso(self, mock_get):
        # Configurar el mock para devolver datos simulados
        mock_get.return_value.json.return_value = {
            'main': {'temp': 300},
            'weather': [{'description': 'sunny', 'icon': '01d'}]
        }

        # Configurar la entrada del usuario
        self.app.ciudad_entry.insert(0, 'CiudadEjemplo')

        # Llamar al método y verificar el resultado
        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()

            mock_mostrar_mensaje.assert_called_with('Clima', 'Temperatura: 26.85°C\nDescripción: Sunny')
            self.assertIsNotNone(self.app.imagen_label.image)

    def test_obtener_clima_error_ciudad_vacia(self):
        with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
            self.app.obtener_clima()

            mock_mostrar_mensaje.assert_called_with('Error', 'Ingresa el nombre de la ciudad')
            self.assertIsNone(self.app.imagen_label.image)

    def test_obtener_clima_error_request(self):
        # Configurar la entrada del usuario
        self.app.ciudad_entry.insert(0, 'CiudadError')

        # Simular un error en la solicitud
        with patch('app_clima.requests.get', side_effect=Exception('Error de red')):
            with patch.object(self.app, 'mostrar_mensaje') as mock_mostrar_mensaje:
                self.app.obtener_clima()

                mock_mostrar_mensaje.assert_called_with('Error', 'Error al obtener el clima: Error de red')
                self.assertIsNone(self.app.imagen_label.image)

if __name__ == '__main__':
    unittest.main()
