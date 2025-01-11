import time

class MinecraftMock:
    """
    Clase principal que sustituye a minecraft.Minecraft.
    Provee métodos básicos que tu bot utiliza: postToChat y acceso a 'events' y 'player'.
    """
    def __init__(self):
        self.chat_log = []        # Simularemos aquí los mensajes que se "publican" en el chat.
        self.events = EventsMock()
        self.player = PlayerMock()

    def postToChat(self, message):
        """
        Simula la publicación de un mensaje en el chat.
        En realidad, lo guardamos en una lista para que pueda ser verificada en los tests.
        """
        print(f"[MinecraftMock] postToChat => {message}")
        self.chat_log.append(message)

class EventsMock:
    """
    Simula events.pollChatPosts() devolviendo los mensajes que "inyectemos".
    """
    def __init__(self):
        # Aquí guardamos mensajes simulados que se hayan "enviado" al servidor.
        self._chat_messages_queue = []

    def pollChatPosts(self):
        """
        Retorna la lista de mensajes encolados y la limpia, para simular la lectura.
        """
        temp = self._chat_messages_queue[:]
        self._chat_messages_queue.clear()
        return temp

    def addChatMessage(self, message, playerId=0):
        """
        Permite a los tests inyectar mensajes de chat que el bot debería 'leer'.
        """
        chat_post = ChatPostMock(message, playerId)
        self._chat_messages_queue.append(chat_post)

class PlayerMock:
    """
    Simula al jugador en Minecraft, devolviendo posiciones predefinidas.
    """
    def __init__(self):
        self.x = 10
        self.y = 64
        self.z = -5

    def getTilePos(self):
        """
        Devuelve un objeto con atributos x, y, z, simulando la posición del jugador.
        """
        return self

class ChatPostMock:
    """
    Estructura que simula un post de chat (mcpi.minecraft.ChatEvent).
    """
    def __init__(self, message, playerId):
        self.message = message
        self.playerId = playerId
        self.timestamp = time.time()
