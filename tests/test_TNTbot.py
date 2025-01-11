import unittest
import time
import threading

from src.TNTbot import (
    set_minecraft_instance,
    main,
    running_tnt_bot
)
from mocks.minecraft_mock import MinecraftMock

class TestTNTBot(unittest.TestCase):

    def setUp(self):
        """
        Se llama antes de cada test:
        1) Creamos el mock de Minecraft.
        2) Inyectamos en el bot.
        3) Ejecutamos main() en un hilo para no bloquear.
        """
        self.mc_mock = MinecraftMock()

        set_minecraft_instance(self.mc_mock)

        self.bot_thread = threading.Thread(target=main, daemon=True)
        self.bot_thread.start()

        # Espera breve para que el bot arranque
        time.sleep(1.0)

    def tearDown(self):
        """
        Después de cada test:
        - Si el bot sigue corriendo, lo detenemos.
        - Join con timeout.
        """
        if running_tnt_bot:
            self.mc_mock.events.addChatMessage("paraTNTbot")
            time.sleep(1.0)

        self.bot_thread.join(timeout=2)

    def test_tnt_flow(self):
        # 1) Verificar mensaje de inicio
        started_ok = any("¡TNT Bot iniciado!" in msg for msg in self.mc_mock.chat_log)
        self.assertTrue(started_ok, "No se encontró el mensaje de inicio del TNT Bot.")

        # 2) Cambiar la frecuencia a 3
        self.mc_mock.events.addChatMessage("setTntFreq 3")
        time.sleep(1.0)  # para que procese

        # Comprobar que respondió "Frecuencia de TNT establecida a 3 s."
        found_freq_msg = any("Frecuencia de TNT establecida a 3" in msg for msg in self.mc_mock.chat_log)
        self.assertTrue(found_freq_msg, "No se encontró el mensaje de frecuencia establecida a 3 s.")

        # 3) Detenemos el bot
        self.mc_mock.events.addChatMessage("paraTNTbot")
        time.sleep(1.0)

        # Guardamos cuántos mensajes había
        final_count = len(self.mc_mock.chat_log)
        # Esperamos un poquito y vemos que no crece
        time.sleep(1.0)
        self.assertEqual(
            final_count,
            len(self.mc_mock.chat_log),
            "Se publicaron mensajes después de detener el TNT Bot."
        )

if __name__ == "__main__":
    unittest.main()
