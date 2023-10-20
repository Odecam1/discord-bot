import discord
from discord.ext import commands
import json

channel_id_member_join = 1164540231484198952
token = "MTE2NDUyNjI1MTAzODQ3NDMxMA.GqT52w.LBoVE9d-Uu4uzwJfH3HfvVq5zyTxX09B7Sv1EI"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)


def save_banned_words(banned_words):
    with open("banned_words.json", "w") as json_file:
        json.dump(banned_words, json_file)


def load_banned_words():
    try:
        with open("banned_words.json", "r") as json_file:
            words = json.load(json_file)
            return words
    except FileNotFoundError:
        save_banned_words([])
        return []


banned_words = load_banned_words()


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


@bot.command(name="aide")
async def help_command(ctx):
    author = ctx.author
    author_permissions = ctx.author.guild_permissions

    # Vérifiez les autorisations de l'utilisateur
    is_admin = author_permissions.administrator
    can_manage_messages = author_permissions.manage_messages

    # Créez un message d'aide en fonction des autorisations de l'utilisateur
    help_message = f"Commandes disponibles pour {author.mention}:\n"

    # Commande générale
    help_message += "!stats - Affiche des informations sur le serveur\n"
    help_message += "!liste_mots_interdits - Affiche la liste des mots interdits\n"

    # Commande réservée aux administrateurs
    if is_admin:
        help_message += "!ajouter_mot_interdit [mots] - Ajoute des mots à la liste des mots interdits\n"
        help_message += "!supprimer_mot_interdit [mots] - Supprime des mots de la liste des mots interdits\n"
        help_message += (
            "!bannisement_membre [utilisateur] [raison] - Bannit un membre du serveur\n"
        )

    # Commande réservée à ceux qui peuvent gérer les messages
    if can_manage_messages:
        help_message += "!clear [nombre] - Supprime un nombre spécifié de messages\n"

    await ctx.send(help_message)


@bot.command(name="stats")
async def server_info(ctx):
    server = ctx.guild
    total_members = len(server.members)
    total_bots = sum(1 for member in server.members if member.bot)
    online_members = 0

    for member in server.members:
        if member.status != discord.Status.offline:
            online_members += 1

    total_channels = 0
    for channel in server.channels:
        if not isinstance(channel, discord.CategoryChannel):
            total_channels += 1

    response = (
        f"Sur le serveur {server.name} :\n"
        f":busts_in_silhouette: Nombre de membres : {total_members} (y compris {total_bots} bots)\n"
        f":hash: Nombre de salons : {total_channels}\n"
        f":green_circle: Nombre de membres en ligne : {online_members}"
    )
    await ctx.send(response)


@bot.command(name="sondage")
async def create_poll(ctx, question, *options):
    poll_embed = discord.Embed(title=question)
    for option in options:
        poll_embed.add_field(name=option, value="0", inline=False)

    poll_message = await ctx.send(embed=poll_embed)

    for i in range(len(options)):
        await poll_message.add_reaction(f"{i+1}\u20e3")


# Commande pour ajouter des mots à la liste de mots interdits (réservée aux modérateurs)
@bot.command(name="ajouter_mot_interdit")
async def add_banned_word(ctx, *words):
    if ctx.author.guild_permissions.administrator:
        words_added = []

        for word in words:
            if word not in banned_words:
                banned_words.append(word)
                words_added.append(word)

        if words_added:
            save_banned_words(banned_words)
            added_msg = (
                f"Mots ajoutés à la liste des mots interdits : {', '.join(words_added)}"
            )

        response = (
            added_msg if words_added else "Aucun mot n'a été spécifié pour ajout."
        )

        if response:
            await ctx.send(response)
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour ajouter un mot interdit."
        )


# Commande pour afficher la liste de mots interdits
@bot.command(name="liste_mots_interdits")
async def list_banned_words(ctx):
    await ctx.send("Liste des mots interdits : " + ", ".join(banned_words))


# Commande pour supprimer un mot de la liste de mots interdits (réservée aux modérateurs)
@bot.command(name="supprimer_mot_interdit")
async def remove_banned_word(ctx, *words):
    if ctx.author.guild_permissions.administrator:
        words_removed = []
        words_not_in_list = []

        for word in words:
            if word in banned_words:
                banned_words.remove(word)
                words_removed.append(word)
            else:
                words_not_in_list.append(word)

        if words_removed:
            save_banned_words(banned_words)
            removed_msg = f"Mots supprimés de la liste des mots interdits : {', '.join(words_removed)}"

        if words_not_in_list:
            not_in_list_msg = f"Mots non présents dans la liste des mots interdits : {', '.join(words_not_in_list)}"

        response = "\n".join(filter(None, [removed_msg, not_in_list_msg]))

        if response:
            await ctx.send(response)
        else:
            await ctx.send("Aucun mot n'a été spécifié pour suppression.")
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour supprimer un mot interdit."
        )


@bot.command(name="bannisement_membre")
async def ban_user(ctx, user: discord.user, *, reason="Aucune raison spécifiée"):
    if ctx.author.guild_permissions.administrator:
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} a été banni pour la raison suivante : {reason}")
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour bannir un utilisateur."
        )


@bot.command()
async def clear(ctx, arg):
    if ctx.author.guild_permissions.manage_messages:
        if arg == "*":
            await ctx.channel.purge()
        else:
            try:
                amount = int(arg)
                if amount <= 0:
                    await ctx.send(
                        "Le nombre de messages à supprimer doit être supérieur à zéro."
                    )
                else:
                    await ctx.channel.purge(
                        limit=amount + 1
                    )  # Le +1 inclut le message de commande lui-même
            except ValueError:
                await ctx.send(
                    "L'argument doit être un nombre ou '*' pour supprimer tous les messages."
                )
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour utiliser cette commande."
        )


bot.run(token)
