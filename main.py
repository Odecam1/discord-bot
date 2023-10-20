import discord
from discord.ext import commands
from util.stats import server_info
from util.banned_words import (
    add_banned_words,
    list_banned_words,
    remove_banned_words,
    check_banned_word,
)
from util.clean import clear
from util.poll import create_poll
from util.ban_members import ban_user


channel_id_member_join = 1164540231484198952
token = "MTE2NDUyNjI1MTAzODQ3NDMxMA.GqT52w.LBoVE9d-Uu4uzwJfH3HfvVq5zyTxX09B7Sv1EI"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} est prêt")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(channel_id_member_join)
    await channel.send(f"Salut {member.mention} ! Bienvenue sur le serveur.")


@bot.event
async def on_message(message):
    if message.author == bot.user:  # Évitez de réagir à vos propres messages
        return

    await check_banned_word(message)
    await bot.process_commands(message)  # Permet au bot de traiter d'autres commandes


commands_list = [
    server_info,
    add_banned_word,
    remove_banned_word,
    list_banned_words,
    clear,
    create_poll,
    ban_user,
]

for command in commands_list:
    bot.add_command(command)


bot.run(token)
