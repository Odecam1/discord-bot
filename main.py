import discord
from discord.ext import commands
import json
import random

CHANNEL_ID = 1164540231484198952
token = "MTE2NDUyNjI1MTAzODQ3NDMxMA.GqT52w.LBoVE9d-Uu4uzwJfH3HfvVq5zyTxX09B7Sv1EI"


def save_banned_words():
    with open("banned_words.json", "w") as json_file:
        json.dump(banned_words, json_file)


def load_banned_words():
    try:
        with open("banned_words.json", "r") as json_file:
            words = json.load(json_file)
            return words
    except FileNotFoundError:
        save_banned_words()
        return []


banned_words = []
banned_words = load_banned_words()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Le bot est prêt.")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Salut {member.mention} ! Bienvenue sur le serveur.")


@bot.command(name="info")
async def server_info(ctx):
    server = ctx.guild
    total_members = len(server.members)
    online_members = sum(
        member.status == discord.Status.online for member in server.members
    )
    total_channels = len(server.text_channels) + len(server.vocal_channels)

    response = f"Nombre total de membres : {total_members}\nMembres en ligne : {online_members}\nNombre de canaux : {total_channels}"
    await ctx.send(response)


@bot.command()
async def create_poll(ctx, question, *options):
    poll_embed = discord.Embed(title=question)
    for option in options:
        poll_embed.add_field(name=option, value="0", inline=False)

    poll_message = await ctx.send(embed=poll_embed)

    for i in range(len(options)):
        await poll_message.add_reaction(f"{i+1}\u20e3")


@bot.event
async def on_message(message):
    if message.author == bot.user:  # Évitez de réagir à vos propres messages
        return

    message_content = (
        message.content.lower()
    )  # Convertir le message en minuscules pour la correspondance insensible à la casse

    for banned_word in banned_words:
        if banned_word in message_content:
            await message.delete()  # Permet au bot de traiter d'autres commandes
            await message.channel.send(
                f"{message.author.mention}, veuillez éviter d'utiliser des mots interdits."
            )
            break

    await bot.process_commands(message)  # Permet au bot de traiter d'autres commandes


# Commande pour ajouter des mots à la liste de mots interdits (réservée aux modérateurs)
@bot.command()
async def add_banned_word(ctx, word):
    if ctx.author.guild_permissions.administrator:
        banned_words.append(word)
        save_banned_words()  # Sauvegarder la liste après modification
        await ctx.send(f"Le mot '{word}' a été ajouté à la liste des mots interdits.")
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour ajouter un mot interdit."
        )


# Commande pour afficher la liste de mots interdits (réservée aux modérateurs)
@bot.command()
async def list_banned_words(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send("Liste des mots interdits : " + ", ".join(banned_words))
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour afficher la liste des mots interdits."
        )


# Commande pour supprimer un mot de la liste de mots interdits (réservée aux modérateurs)
@bot.command()
async def remove_banned_word(ctx, word):
    if ctx.author.guild_permissions.administrator:
        if word in banned_words:
            banned_words.remove(word)
            save_banned_words()
            await ctx.send(
                f"Le mot '{word}' a été supprimé de la liste des mots interdits."
            )
        else:
            await ctx.send(
                f"Le mot '{word}' n'est pas dans la liste des mots interdits."
            )
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour supprimer un mot interdit."
        )


bot.run(token)
