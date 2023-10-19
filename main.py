import discord
from discord.ext import commands
import json
import random

CHANNEL_ID = ""
token = ""


def charger_mots_interdits():
    try:
        with open("mots_interdits.json", "r") as json_file:
            mots = json.load(json_file)
            return mots
    except FileNotFoundError:
        return ["mot1", "mot2", "mot3"]


mots_interdits = charger_mots_interdits()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Salut {member.mention} ! Bienvenue sur le serveur.")


@bot.command()
async def server_info(ctx):
    server = ctx.guild
    total_members = len(server.members)
    online_members = sum(
        member.status == discord.Status.online for member in server.members
    )
    total_channels = len(server.channels)

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

    contenu_message = (
        message.content.lower()
    )  # Convertir le message en minuscules pour la correspondance insensible à la casse

    for mot_interdit in mots_interdits:
        if mot_interdit in contenu_message:
            await message.delete()  # Supprimer le message s'il contient un mot interdit
            await message.channel.send(
                f"{message.author.mention}, veuillez éviter d'utiliser des mots interdits."
            )
            break

    await bot.process_commands(message)  # Permet au bot de traiter d'autres commandes


def sauvegarder_mots_interdits():
    with open("mots_interdits.json", "w") as json_file:
        json.dump(mots_interdits, json_file)


# Commande pour ajouter des mots à la liste de mots interdits (réservée aux modérateurs)
@bot.command()
async def ajouter_mot_interdit(ctx, mot):
    if ctx.author.guild_permissions.administrator:
        mots_interdits.append(mot)
        sauvegarder_mots_interdits()  # Sauvegarder la liste après modification
        await ctx.send(f"Le mot '{mot}' a été ajouté à la liste des mots interdits.")
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour ajouter un mot interdit."
        )


# Commande pour afficher la liste de mots interdits (réservée aux modérateurs)
@bot.command()
async def liste_mots_interdits(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.send("Liste des mots interdits : " + ", ".join(mots_interdits))
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour afficher la liste des mots interdits."
        )


# Commande pour supprimer un mot de la liste de mots interdits (réservée aux modérateurs)
@bot.command()
async def supprimer_mot_interdit(ctx, word):
    if ctx.author.guild_permissions.administrator:
        if word in mots_interdits:
            mots_interdits.remove(word)
            sauvegarder_mots_interdits()
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
