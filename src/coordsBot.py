import threading
import time
import functools
import queue

# Cola para comunicar mensajes al test o a otros consumidores.
message_queue = queue.Queue()

# Variable global que contendrá la instancia de Minecraft (mock o real).
mc = None

def set_minecraft_instance(minecraft_instance):
    """
    Asigna la instancia (mock o real) de Minecraft que se usará en el bot.
    """
    global mc
    mc = minecraft_instance

# ==============================
#   FUNCIONES DE COORDENADAS
# ==============================
def get_player_coords():
    pos = mc.player.getTilePos()
    return (pos.x, pos.y, pos.z)

def coords_to_message(coords, mode="normal"):
    if mode == "positive":
        transformed = list(map(abs, coords))
    elif mode == "negative":
        transformed = list(map(lambda c: -abs(c), coords))
    else:
        transformed = coords

    str_coords = map(str, transformed)
    joined_coords = functools.reduce(lambda a, b: a + ", " + b, str_coords)
    return f"Coordenadas ({mode}): {joined_coords}"

# ===========================
#     HILO DE ESCUCHA CHAT
# ===========================
def chat_listener():
    running = True
    while running:
        chat_messages = mc.events.pollChatPosts()
        for post in chat_messages:
            msg = post.message.lower().strip()

            if msg == "getcoords":
                coords = get_player_coords()
                message = coords_to_message(coords, mode="normal")
                mc.postToChat(message)
                message_queue.put(message)  # Encolar el mensaje
                print(message)

            elif msg == "getpositivecoords":
                coords = get_player_coords()
                message = coords_to_message(coords, mode="positive")
                mc.postToChat(message)
                message_queue.put(message)
                print(message)

            elif msg == "getnegativecoords":
                coords = get_player_coords()
                message = coords_to_message(coords, mode="negative")
                mc.postToChat(message)
                message_queue.put(message)
                print(message)

            elif msg == "paracoordsbot":
                running = False
                stop_message = "Bot de coordenadas detenido."
                mc.postToChat(stop_message)
                message_queue.put(stop_message)
                print("Bot de coordenadas detenido por comando.")

        time.sleep(0.2)

# ==========================
#    EJECUCIÓN PRINCIPAL
# ==========================
def main():
    mc.postToChat("Bot coords iniciado.")
    mc.postToChat("Comandos: getCoords, getPositiveCoords, getNegativeCoords, paraCoordsBot.")

    # Crear y arrancar el hilo que escucha el chat
    listener_thread = threading.Thread(target=chat_listener, daemon=True)
    listener_thread.start()

    # Mantener el hilo principal vivo hasta que se detenga el bot
    listener_thread.join()

if __name__ == "__main__":
    # Si se ejecuta directamente, asumimos instancia REAL de Minecraft.
    from libs.mcpi.minecraft import Minecraft
    set_minecraft_instance(Minecraft.create())
    main()
