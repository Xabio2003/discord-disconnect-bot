import asyncio
import http.server
import os
import threading
import discord
from discord.ext import commands

# Servidor web falso para mantener contento a Render
PORT = int(os.environ.get("PORT", 10000))


class SimpleHandler(http.server.BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is alive!")


def run_web_server():
  server = http.server.HTTPServer(("0.0.0.0", PORT), SimpleHandler)
  server.serve_forever()


threading.Thread(target=run_web_server, daemon=True).start()

# Configuración de Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Bot conectado como {bot.user}")


@bot.command(name="desconectar")
async def desconectar(ctx, miembro: discord.Member, minutos: int):
  try:
    if not miembro.voice or not miembro.voice.channel:
      await ctx.send(
          f"⚠️ {miembro.mention} no está en un canal de voz, pero el temporizador"
          " se activará igual."
      )

    await ctx.send(
        f"⏳ **Temporizador iniciado:** {miembro.display_name} será desconectado"
        f" en **{minutos} minuto(s)**."
    )

    await asyncio.sleep(minutos * 60)

    if miembro.voice and miembro.voice.channel:
      try:
        await miembro.move_to(None)
        await ctx.send(
            f"🔌 El tiempo ha terminado. {miembro.mention} ha sido desconectado"
            " del canal de voz."
        )
      except discord.Forbidden:
        await ctx.send(
            "❌ **Error de permisos:** El bot no tiene permiso de **Mover"
            " Miembros** en el servidor, o el rol del bot está por debajo del"
            " usuario que intentas sacar."
        )
      except Exception as e:
        await ctx.send(f"❌ No pude desconectar a {miembro.display_name}: {e}")
    else:
      await ctx.send(
          f"⏱️ El tiempo terminó, pero {miembro.display_name} ya había salido del"
          " canal por su cuenta."
      )
  except Exception as e:
    await ctx.send(f"❌ Ocurrió un error inesperado: {e}")


bot.run(os.getenv("DISCORD_TOKEN"))
