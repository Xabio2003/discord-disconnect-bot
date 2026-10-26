import asyncio
import http.server
import os
import threading
import discord
from discord.ext import commands

# --- Servidor HTTP falso para mantener contento a Render ---
PORT = int(os.environ.get("PORT", 10000))


class SimpleHandler(http.server.BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is alive!")


def run_web_server():
  server = http.server.HTTPServer(("0.0.0.0", PORT), SimpleHandler)
  server.serve_forever()


# Iniciar el servidor web en segundo plano
threading.Thread(target=run_web_server, daemon=True).start()

# --- Configuración del Bot de Discord ---
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
  print(f"Bot conectado como {bot.user}")


@bot.command(name="desconectar", help="Desconecta a un usuario tras X minutos.")
@commands.has_permissions(move_members=True)
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

  await asyncio.sleep(minutos * 60)

  if miembro.voice and miembro.voice.channel:
    try:
      await miembro.move_to(None)
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


bot.run(os.getenv("DISCORD_TOKEN"))
