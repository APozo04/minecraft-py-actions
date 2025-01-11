import threading
import time
import random
from functools import reduce

try:
    import libs.mcpi.minecraft as minecraft
except ImportError:
    minecraft = None # Si no esta disponible mcpi se usará mock (modo test)

# =========================
#    VARIABLES GLOBALES
# =========================
mc = None  # Se inyectará o la instancia real, o un mock
running_insult_bot = True
insult_delay = 5 # Delay entre insultos (segundos)
current_transformation = None  # Transformación dinámica seleccionada

# NUEVA VARIABLE PARA PAUSAR INSULTOS
insults_paused = False

# =========================
#    LISTA DE INSULTOS
# =========================
INSULTS = [
    "tonto",
    "feo",
    "menso",
    "torpe",
    "baboso",
    "fan del real madrid",
    "bobo",
    "cateto",
    "zoquete",
    "cara anchoa"
]

# =========================
#   TRANSFORMACIONES (FUNCIONALES)
# =========================
TRANSFORMATIONS = {
    "uppercase": lambda s: s.upper(),
    "lowercase": lambda s: s.lower(),
    "reverse": lambda s: s[::-1],
    "capitalize": lambda s: s.capitalize(),
    "title": lambda s: s.title(),
    "swapcase": lambda s: s.swapcase(),
    "doubled": lambda s: ''.join(ch * 2 for ch in s)
}

# =========================
#     GENERADORES
# =========================
def random_insult_generator():
    """Generador infinito de insultos al azar."""
    while True:
        yield random.choice(INSULTS)

def transform_insult(insult):
    """
    Aplica una transformación dinámica al insulto si está definida,
    de lo contrario lo devuelve sin cambios.
    """
    global current_transformation
    if current_transformation and current_transformation in TRANSFORMATIONS:
        transformation = TRANSFORMATIONS[current_transformation]
        return transformation(insult)
    return insult

# =========================
#   BOT DE INSULTOS
# =========================
def insult_bot():
    """
    Publica insultos transformados dinámicamente en el chat,
    mientras running_insult_bot sea True.
    Se pausa si insults_paused es True.
    """
    global running_insult_bot
    global insult_delay
    global mc
    global insults_paused

    insult_stream = random_insult_generator()

    for insult in insult_stream:
        # Si el bot está detenido, rompemos el ciclo.
        if not running_insult_bot:
            break

        # Si está en pausa, esperamos hasta que se reanude.
        while insults_paused and running_insult_bot:
            time.sleep(0.2)

        # Verificamos de nuevo si alguien detuvo el bot mientras estaba pausado.
        if not running_insult_bot:
            break

        transformed_insult = transform_insult(insult)
        mc.postToChat(transformed_insult)
        print(f"[InsultBot] Insulto publicado: {transformed_insult}")
        time.sleep(insult_delay)

def listen_for_stop_command():
    """
    Hilo que escucha el chat:
    - "paraInsultBot" detiene el bot.
    - "setInsultFreq X" cambia el delay global a X (máx 10).
    - "listTransformations" lista las transformaciones disponibles y PAUSA el flujo.
    - "setTransformation NAME" cambia la transformación dinámica.
    - "helpInsult" muestra los comandos disponibles y PAUSA el flujo.
    - "addInsult x" añade un nuevo insulto a la lista.
    - "continueInsult" reanuda el flujo de insultos si está pausado.
    """
    global running_insult_bot
    global insult_delay
    global current_transformation
    global mc
    global INSULTS
    global insults_paused

    while running_insult_bot:
        chat_posts = mc.events.pollChatPosts()
        for post in chat_posts:
            msg = post.message.lower().strip()

            if msg == "parainsultbot":
                running_insult_bot = False
                mc.postToChat("InsultBot detenido!")
                print("[InsultBot] Bot detenido por comando de chat.")

            elif msg.startswith("setinsultfreq"):
                parts = msg.split()
                if len(parts) == 2 and parts[1].isdigit():
                    new_delay = int(parts[1])
                    if new_delay > 10:
                        new_delay = 10
                    insult_delay = new_delay
                    mc.postToChat(f"Frecuencia de insultos cambiada a {new_delay}s")
                    print(f"[InsultBot] Nueva frecuencia de insultos: {new_delay}s")
                else:
                    mc.postToChat("Uso correcto: setInsultFreq <número>")

            elif msg == "listtransformations":
                available = ", ".join(TRANSFORMATIONS.keys())
                mc.postToChat(f"Transformaciones disponibles: {available}")
                mc.postToChat("Escribe 'continueInsult' para seguir con el flujo de los insultos.")
                print(f"[InsultBot] Transformaciones disponibles: {available}")
                insults_paused = True  # Pausar insultos

            elif msg.startswith("settransformation"):
                parts = msg.split()
                if len(parts) == 2 and parts[1] in TRANSFORMATIONS:
                    current_transformation = parts[1]
                    mc.postToChat(f"Transformacion activa: {current_transformation}")
                    print(f"[InsultBot] Transformación activa: {current_transformation}")
                else:
                    mc.postToChat("Transformacion no válida. Usa 'listTransformations'.")

            elif msg == "helpinsult":
                mc.postToChat("Comandos disponibles:")
                mc.postToChat("- paraInsultBot: Detiene el bot.")
                mc.postToChat("- setInsultFreq X: Cambia la frecuencia de insultos (max 10 s).")
                mc.postToChat("- listTransformations: Lista las transformaciones disponibles.")
                mc.postToChat("- setTransformation NAME: Cambia la transformacion dinamica.")
                mc.postToChat("- addInsult x: Añade un nuevo insulto a la lista.")
                mc.postToChat("- continueInsult: Reanuda el flujo de insultos si esta pausado.")
                mc.postToChat("Escribe 'continueInsult' para seguir con el flujo de los insultos.")
                print("[InsultBot] Mensaje de ayuda enviado.")
                insults_paused = True  # Pausar insultos

            elif msg.startswith("addinsult"):
                parts = msg.split(maxsplit=1)
                if len(parts) == 2:
                    new_insult = parts[1].strip()
                    if new_insult:
                        INSULTS.append(new_insult)
                        mc.postToChat(f"Nuevo insulto añadido: {new_insult}")
                        print(f"[InsultBot] Insulto añadido: {new_insult}")
                    else:
                        mc.postToChat("Error: no se especificó el insulto a añadir.")
                else:
                    mc.postToChat("Uso correcto: addInsult <insulto>")

            elif msg == "continueinsult":
                # Reanudar insultos si estaban pausados
                if insults_paused:
                    insults_paused = False
                    mc.postToChat("El bot de insultos continua!")
                    print("[InsultBot] Insultos reanudados.")
                else:
                    mc.postToChat("El flujo de insultos ya está activo.")

        time.sleep(0.2)

# =========================
#    INYECCIÓN DE MC
# =========================
def set_minecraft_instance(instance):
    """
    Asigna la instancia (mock o real) de Minecraft que se usará en el bot.
    """
    global mc
    mc = instance

# =========================
#     EJECUCIÓN PRINCIPAL
# =========================
def main():
    """
    Arranca el bot de insultos en hilos separados (insulto + escucha).
    Si no hay instancia de Minecraft configurada, se asume la real.
    """
    global mc
    global running_insult_bot

    # Si no hay instancia configurada aún, usamos la real.
    if mc is None:
        set_minecraft_instance(minecraft.Minecraft.create())

    # Reiniciamos banderas por si se ha corrido antes
    running_insult_bot = True

    mc.postToChat("InsultBot iniciado! Escribe 'paraInsultBot' para detenerlo.")
    mc.postToChat("Escribe 'helpInsult' para ver los comandos disponibles.")

    bot_thread = threading.Thread(target=insult_bot, daemon=True)
    stop_thread = threading.Thread(target=listen_for_stop_command, daemon=True)
    bot_thread.start()
    stop_thread.start()

    bot_thread.join()
    stop_thread.join()


if __name__ == "__main__":
    main()
