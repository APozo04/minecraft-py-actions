import mcpi.minecraft as minecraft
import mcpi.block as block

# Conectar al servidor de Minecraft
mc = minecraft.Minecraft.create()

# Obtener las coordenadas del jugador
pos = mc.player.getTilePos()
print(f"Las coordenadas actuales del jugador son: {pos.x}, {pos.y}, {pos.z}")
mc.postToChat(f"Las coordenadas actuales del jugador son: {pos.x}, {pos.y}, {pos.z}")