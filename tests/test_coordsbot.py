import unittest
import time
import threading

from src.coordsBot import (
    set_minecraft_instance,
    chat_listener,
    message_queue
)
from mocks.minecraft_mock import MinecraftMock

class TestCoordsBot(unittest.TestCase):
    def setUp(self):
        """
        Se llama antes de cada test individual.
        Configura el bot con el mock de Minecraft y limpia la cola de mensajes.
        """
        self.minecraft_mock = MinecraftMock()
        set_minecraft_instance(self.minecraft_mock)

        # Asegurarnos de que la cola esté vacía.
        while not message_queue.empty():
            message_queue.get()

        # Iniciar el hilo del bot.
        self.listener_thread = threading.Thread(target=chat_listener, daemon=True)
        self.listener_thread.start()
        time.sleep(0.2)  # Dar un poquito de tiempo para que el bot arranque.

    def tearDown(self):
        """
        Se llama después de cada test individual.
        Aseguramos que el hilo se detenga enviando 'paraCoordsBot'.
        """
        self.minecraft_mock.events.addChatMessage("paraCoordsBot")
        # Esperar a que el bot procese el mensaje de parada.
        time.sleep(0.5)
        # Verificar si se generó el mensaje de parada.
        while not message_queue.empty():
            msg = message_queue.get()
            if msg.startswith("Bot de coordenadas detenido."):
                break
        # Hacemos un join con timeout en caso de que ya haya finalizado.
        self.listener_thread.join(timeout=1)

    def test_get_coords_normal(self):
        """
        Prueba que el bot responda a 'getCoords' con las coordenadas en modo 'normal'.
        """
        self.minecraft_mock.events.addChatMessage("getCoords")
        # Esperamos a leer algo de la cola.
        response = self._wait_for_bot_response(prefix="Coordenadas (normal):")
        self.assertIn("Coordenadas (normal):", response)

    def test_get_coords_positive(self):
        """
        Prueba que el bot responda a 'getPositiveCoords' con las coordenadas positivas.
        """
        self.minecraft_mock.events.addChatMessage("getPositiveCoords")
        response = self._wait_for_bot_response(prefix="Coordenadas (positive):")
        self.assertIn("Coordenadas (positive):", response)

    def test_get_coords_negative(self):
        """
        Prueba que el bot responda a 'getNegativeCoords' con las coordenadas negativas.
        """
        self.minecraft_mock.events.addChatMessage("getNegativeCoords")
        response = self._wait_for_bot_response(prefix="Coordenadas (negative):")
        self.assertIn("Coordenadas (negative):", response)

    def _wait_for_bot_response(self, prefix, timeout=2):
        """
        Espera hasta `timeout` segundos a que llegue un mensaje en message_queue
        que empiece con 'prefix'. Si no aparece, lanza una excepción.
        """
        start = time.time()
        while time.time() - start < timeout:
            if not message_queue.empty():
                msg = message_queue.get()
                if msg.startswith(prefix):
                    return msg
            time.sleep(0.1)
        raise TimeoutError(f"No se recibió el mensaje con prefijo '{prefix}' en {timeout} segundos.")

if __name__ == "__main__":
    unittest.main()
