import unittest
import time
import threading

# Importamos todo lo necesario de insult_bot
from src.insultBot import (
    set_minecraft_instance,
    main,
    running_insult_bot,
    insult_delay,
    current_transformation
)

# Importamos el mock
from mocks.minecraft_mock import MinecraftMock


class TestInsultBot(unittest.TestCase):

    def setUp(self):
        """
        Se llama antes de cada test:
        1. Crea el mock de Minecraft.
        2. Lo inyecta en insult_bot.
        3. Ejecuta main() en un hilo para no bloquear.
        """
        self.mc_mock = MinecraftMock()
        set_minecraft_instance(self.mc_mock)

        self.bot_thread = threading.Thread(target=main, daemon=True)
        self.bot_thread.start()

        # Pequeña espera para que el bot arranque
        time.sleep(1.0)

    def tearDown(self):
        """
        Después de cada test:
        - Detenemos el bot si sigue corriendo, y esperamos a que pare.
        """
        if running_insult_bot:
            self.mc_mock.events.addChatMessage("paraInsultBot")
            time.sleep(1.0)  # Damos tiempo a que procese el comando

        self.bot_thread.join(timeout=2)

    def test_insult_bot_flow(self):
        """
        Verifica en un flujo continuo que:
        - Llegan insultos por defecto.
        - Se pausa con 'listTransformations'.
        - Se reanuda con 'continueInsult'.
        - 'setTransformation uppercase' funciona.
        - 'addInsult' se añade correctamente.
        - 'setInsultFreq 1' cambia la frecuencia.
        - 'paraInsultBot' detiene todo.
        """

        # 1) Esperar al menos 1 insulto (por defecto: cada 5s).
        self._wait_for_insults(min_count=1, timeout=6)

        # 2) listTransformations => pausar el bot
        # Enviamos el comando
        self.mc_mock.events.addChatMessage("listTransformations")

        # Esperamos a que el bot publique "Transformaciones disponibles:"
        # → esto confirma que YA procesó el comando y, por tanto, se ha pausado
        self._wait_for_message("Transformaciones disponibles:", timeout=2.0)

        # Contamos cuántos mensajes hay justo ahora (incluyendo el que anuncia la pausa)
        start_count = len(self.mc_mock.chat_log)

        # Esperamos 2s más y comprobamos que NO se publican insultos nuevos en pausa
        time.sleep(2.0)
        self.assertEqual(
            start_count,
            len(self.mc_mock.chat_log),
            "El bot publicó insultos mientras estaba en pausa."
        )

        # 3) Reanudamos con continueInsult
        self.mc_mock.events.addChatMessage("continueInsult")
        time.sleep(0.5)

        # Ahora esperamos que se publique al menos 1 insulto más
        self._wait_for_insults(min_count=start_count + 1, timeout=6)

        # 4) setTransformation uppercase => verificamos que salen en mayúsculas
        self.mc_mock.events.addChatMessage("setTransformation uppercase")
        time.sleep(1.0)  # Damos un margen para que el bot lo procese

        # Esperamos 2 insultos nuevos
        old_count = len(self.mc_mock.chat_log)
        self._wait_for_insults(min_count=old_count + 2, timeout=8)

        # Revisamos que los 2 últimos "insultos" vengan en mayúsculas
        last_two = self.mc_mock.chat_log[-2:]
        for msg in last_two:
            # Filtramos posibles mensajes "Transformacion activa: uppercase"
            # Buscamos insultos genuinos, comprobando que su parte alfabética esté en mayúsculas
            if "Transformacion activa:" in msg:
                continue
            letters_only = "".join(ch for ch in msg if ch.isalpha())
            self.assertTrue(
                letters_only.isupper(),
                f"Se esperaba un insulto en mayúsculas, pero se obtuvo: {msg}"
            )

        # 5) addInsult "supertonto"
        self.mc_mock.events.addChatMessage("addInsult supertonto")
        time.sleep(0.5)
        # Verificamos que se publicó el mensaje de confirmación
        self.assertIn(
            "Nuevo insulto añadido: supertonto",
            self.mc_mock.chat_log,
            "No se encontró el mensaje de confirmación de addInsult."
        )

        # 6) setInsultFreq 1 => chequeamos que la variable global cambie
        self.mc_mock.events.addChatMessage("setInsultFreq 1")
        time.sleep(1.0)
        from src.insultBot import insult_delay
        self.assertEqual(
            insult_delay,
            1,
            "No se actualizó la frecuencia de insultos a 1 segundo."
        )

        # Esperamos que lleguen al menos 2 insultos con la nueva frecuencia (1s) en ~5 seg
        prev_count = len(self.mc_mock.chat_log)
        self._wait_for_insults(min_count=prev_count + 2, timeout=5)

        # 7) Detenemos el bot
        self.mc_mock.events.addChatMessage("paraInsultBot")
        time.sleep(1.0)

        final_count = len(self.mc_mock.chat_log)
        # Esperamos un poquito y comprobamos que NO se publican más insultos
        time.sleep(2.0)
        self.assertEqual(
            final_count,
            len(self.mc_mock.chat_log),
            "Se publicaron insultos después de detener el bot."
        )

    # =======================
    #    MÉTODOS AUXILIARES
    # =======================
    def _wait_for_insults(self, min_count, timeout=5):
        """
        Espera hasta 'timeout' segundos a que self.mc_mock.chat_log
        tenga al menos 'min_count' mensajes. Lanza AssertionError si no sucede.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if len(self.mc_mock.chat_log) >= min_count:
                return
            time.sleep(0.3)
        raise AssertionError(
            f"No se alcanzó la cantidad mínima de {min_count} insultos en {timeout} s. "
            f"Sólo hay {len(self.mc_mock.chat_log)}."
        )

    def _wait_for_message(self, substring, timeout=3.0):
        """
        Espera hasta 'timeout' segundos a que aparezca un mensaje en
        self.mc_mock.chat_log que contenga 'substring'. Lanza AssertionError si no sucede.
        """
        start = time.time()
        while time.time() - start < timeout:
            # Buscamos en todos los mensajes ya registrados
            for msg in self.mc_mock.chat_log:
                if substring in msg:
                    return
            time.sleep(0.2)
        raise AssertionError(
            f"No apareció el mensaje que contiene '{substring}' en {timeout}s."
        )


if __name__ == "__main__":
    unittest.main()
