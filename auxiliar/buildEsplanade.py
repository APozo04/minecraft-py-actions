import libs.mcpi.minecraft as minecraft
import libs.mcpi.block as block

# Conectar con el servidor de Minecraft
mc = minecraft.Minecraft.create()

# Obtener la posición del jugador
player_pos = mc.player.getTilePos()

# Coordenadas iniciales para construir la esplanada, en frente del jugador
x = player_pos.x + 5
y = player_pos.y
z = player_pos.z + 5

# Dimensiones de la esplanada (cuadrada)
size = 100  # Tamaño del cuadrado (1000x1000)

# Construir la esplanada con bloques de piedra
def build_square(x, y, z, size, block_type):
    for i in range(size):
        for j in range(size):
            mc.setBlock(x + i, y, z + j, block_type)

# Llamar a la función para crear la esplanada cuadrada
build_square(x, y, z, size, block.STONE.id)  # Usando bloques de piedra

# Postear en el chat cuando termine de construir la esplanada
mc.postToChat("Square esplanade of stone blocks built in front of you!")
