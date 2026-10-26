import asyncio
import os
import discord
from discord.ext import commands

# Configurar intents necesarios
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Bot conectado como {bot.user}")


@bot.command(name="desconectar", help="Desconecta a un usuario tras X minutos.")
@commands.has_permissions(
    move_members=True
)  # Requiere permiso de mover miembros en Discord
async def desconectar(ctx, miembro: discord.Member, minutos: int):
  if not miembro.voice or not miembro.voice.channel:
    await ctx.send(
        f"⚠️ {miembro.mention} no está en un canal de voz, pero el temporizador"
        " se activará igual."
    )

  await ctx.send(
      f"⏳ **Temporizador iniciado:** {miembro.display_name} será desconectado"
      f" en **{minutos} minuto(s)**."
  )

  # Esperar el tiempo indicado (convertido a segundos)
  await asyncio.sleep(minutos * 60)

  # Comprobar si todavía sigue en el canal de voz al terminar el tiempo
  if miembro.voice and miembro.voice.channel:
    try:
      await miembro.move_to(None)  # Esto lo saca del canal de voz
      await ctx.send(
          f"🔌 El tiempo ha terminado. {miembro.mention} ha sido desconectado"
          " del canal de voz."
      )
    except Exception as e:
      await ctx.send(f"❌ No pude desconectar a {miembro.display_name}: {e}")
  else:
    await ctx.send(
        f"⏱️ El tiempo terminó, pero {miembro.display_name} ya había salido del"
        " canal por su cuenta."
    )


# El token se toma de forma segura de las variables del servidor en la nube
bot.run(os.getenv("DISCORD_TOKEN"))