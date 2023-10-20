import discord
from discord.ext import commands
from util.stats import server_info
from util.banned_words import (
    add_banned_word,
    list_banned_words,
    remove_banned_word,
    banned_words,
)
from util.clean import clear
from util.poll import create_poll

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

    message_content = (
        message.content.lower()
    )  # Convertir le message en minuscules pour la correspondance insensible à la casse

    for banned_word in banned_words:
        if banned_word in message_content:
            await message.delete()  # Supprimer le message s'il contient un mot interdit
            await message.channel.send(
                f"{message.author.mention}, veuillez éviter d'utiliser des mots interdits."
            )
            break

    await bot.process_commands(message)  # Permet au bot de traiter d'autres commandes


bot.add_command(server_info)
bot.add_command(add_banned_word)
bot.add_command(remove_banned_word)
bot.add_command(list_banned_words)
bot.add_command(clear)
bot.add_command(create_poll)


@bot.command(name="bannisement_membre")
async def ban_user(ctx, user: discord.user, *, reason="Aucune raison spécifiée"):
    if ctx.author.guild_permissions.administrator:
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} a été banni pour la raison suivante : {reason}")
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour bannir un utilisateur."
        )


bot.run(token)
