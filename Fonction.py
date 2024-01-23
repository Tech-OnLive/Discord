import discord
import json
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from datetime import time

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_reaction_add(reaction, user):
    required_role_name = "DIGGERS/LFDM"

    if isinstance(user, discord.Member):
        if any(role.name == required_role_name for role in user.roles):
            if reaction.emoji == "📌":
                message = reaction.message
                message_data = {
                    'content': message.content
                }

                # Enregistre les données dans un fichier JSON
                with open('MessageDuJour.json', 'a') as f:
                    json.dump(message_data, f)
                    f.write('\n')

@bot.command(name='auj')
async def auj(ctx):
    required_role_name = "DIGGERS/LFDM"

    # Vérifie si l'auteur du message a le rôle requis
    if any(role.name == required_role_name for role in ctx.author.roles):
        try:
            # Ouvre et lit le fichier des message enregistrés
            with open('MessageDuJour.json', 'r') as f:
                response = ''
                for line in f:
                    message_data = json.loads(line)
                    response += f"{message_data['content']}\n"

            # Envoie un message avec tous les messages enregistrés
            if response:
                await ctx.send(response)
            else:
                await ctx.send("Pas de message enregistré aujourd'hui.")
        except FileNotFoundError:
            await ctx.send("Pas de fichier avec les messages.")
        except Exception as e:
            await ctx.send(f"Erreur: {e}")

scheduler = AsyncIOScheduler(timezone="Europe/Paris")

def clear_json():
    try:
        with open('MessageDuJour.json', 'w') as f:
            f.truncate(0)
        print("Fichier JSON vidé.")
    except Exception as e:
        print(f"Erreur lors de la vidange du fichier JSON: {e}")

scheduler.add_job(clear_json, 'cron', hour=3, minute=47)

scheduler.start()

bot.run('MTE5NTc4MzQ1MTg0NTA4MzIzNw.GhfDcY.JXzP-2etQTteiD5Chci4_-ePnQmiSaNXpMjyg8')
