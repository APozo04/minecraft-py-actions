# tnt_bot.py
# -*- coding: utf-8 -*-

import time
import random
from functools import partial

# Intentamos importar la librería mcpi (real)
try:
    import libs.mcpi.minecraft as minecraft
    import libs.mcpi.block as block
except ImportError:
    # Si no está disponible, se usará un mock que inyectaremos en test
    minecraft = None
    block = None

# =========================================
#  VARIABLES GLOBALES / CONFIGURACIÓN
# =========================================
mc = None  # Se inyecta (mock o real) con set_minecraft_instance()
running_tnt_bot = True  # Flag global para saber si sigue ejecutándose
default_delay = 5

# =========================================
#     INYECCIÓN DE MC
# =========================================
def set_minecraft_instance(instance):
    """
    Permite inyectar la instancia de Minecraft (mock o real) que usará el bot.
    """
    global mc
    mc = instance

# =========================================
#     FUNCIONES AUXILIARES
# =========================================
def get_player_position_safe():
    """
    Devuelve la posición (x, y, z) del jugador o None si falla.
    """
    try:
        pos = mc.player.getTilePos()
        return (pos.x, pos.y, pos.z)
    except Exception as e:
        print(f"Error al obtener las coordenadas del jugador: {e}")
        return None

def random_coordinates_around(x, y, z, radius):
    """
    Genera coordenadas aleatorias en un radio 'radius' alrededor de (x, y, z).
    """
    return (
        x + random.randint(-radius, radius),
        y + random.randint(-1, 2),  # pequeña variación vertical
        z + random.randint(-radius, radius),
    )

def place_tnt_and_fire(x, y, z):
    """
    Coloca TNT en (x, y, z) y fuego en (x, y-1, z).
    """
    try:
        # Si `block` es None porque no hay mcpi real,
        # asumimos que el mock sabrá manejar setBlock o IDs.
        mc.setBlock(x, y, z, block.TNT.id)
        mc.setBlock(x, y - 1, z, block.FIRE.id)
    except Exception as e:
        print(f"Error al colocar TNT y FUEGO: {e}")

def process_chat_command(command, args, current_delay):
    """
    Procesa los comandos de chat.
    - "paraTNTbot" => detiene el bot
    - "setTntFreq X" => cambia la frecuencia (1..10)
    Devuelve el nuevo `delay`.
    """
    global running_tnt_bot

    if command == "paratntbot":
        mc.postToChat("Deteniendo TNT Bot...")
        running_tnt_bot = False

    elif command == "settntfreq":
        try:
            freq = int(args[0])
            freq = max(1, min(freq, 10))  # Limitar entre 1 y 10
            mc.postToChat(f"Frecuencia de TNT establecida a {freq} s.")
            return freq
        except (ValueError, IndexError):
            mc.postToChat("Error: 'setTntFreq X' => X debe ser un número.")

    return current_delay

# =========================================
#  LÓGICA PRINCIPAL DEL BOT
# =========================================
def tnt_bot_main():
    """
    Bucle principal del TNT Bot.
    - Publica mensaje de inicio.
    - Cada 'delay' s coloca TNT cerca del jugador.
    - Escucha comandos para cambiar delay o detener.
    """
    global running_tnt_bot
    running_tnt_bot = True  # Reiniciamos por si se usó antes

    radius = 5
    delay = default_delay
    last_tnt_time = time.time()

    mc.postToChat("¡TNT Bot iniciado! Escribe 'paraTNTbot' para detenerlo.")
    mc.postToChat("Usa 'setTntFreq X' para cambiar la frecuencia (máx: 10 s).")

    while running_tnt_bot:
        # 1) Procesar comandos de chat
        try:
            messages = mc.events.pollChatPosts()
            for msg in messages:
                user_input = msg.message.lower().strip().split()
                if user_input:
                    command, args = user_input[0], user_input[1:]
                    delay = process_chat_command(command, args, delay)
        except Exception as e:
            print(f"Error al escuchar comandos: {e}")

        # 2) Colocar TNT cada 'delay' seg
        now = time.time()
        if now - last_tnt_time >= delay:
            player_pos = get_player_position_safe()
            if player_pos:
                # Generamos coords y colocamos TNT
                generate_coordinates = partial(random_coordinates_around, *player_pos, radius)
                tnt_coords = generate_coordinates()
                place_tnt_and_fire(*tnt_coords)

            last_tnt_time = now

        # 3) Pequeña pausa
        time.sleep(0.1)

    # Cuando se salga del while (bot detenido)
    mc.postToChat("TNT Bot detenido. ¡Hasta la próxima!")

def main():
    """
    Si mc no está configurado, usamos la instancia real de Minecraft (mcpi).
    Después lanzamos el bot principal.
    """
    global mc
    if mc is None:
        # Asumimos que tenemos las librerías mcpi reales
        mc = minecraft.Minecraft.create()

    tnt_bot_main()

if __name__ == "__main__":
    main()
