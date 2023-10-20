from discord.ext import commands
from util.json_ban_word import save_banned_words, banned_words


# Commande pour ajouter des mots à la liste de mots interdits (réservée aux modérateurs)
@commands.command(name="ajouter_mot_interdit")
async def add_banned_word(ctx, *words):
    if ctx.author.guild_permissions.administrator:
        words_added = []

        if words:
            for word in words:
                if not word in banned_words:
                    banned_words.append(word)
                    words_added.append(word)
        else:
            response = "Aucun mot n'a été spécifié pour ajout."

        if words_added:
            save_banned_words(banned_words)
            response = (
                f"Mots ajoutés à la liste des mots interdits : {', '.join(words_added)}"
            )
        else:
            response = "Aucun mot n'a été ajouter car ils sont tous dans la liste"

        if response:
            await ctx.send(response)

    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour ajouter un mot interdit."
        )


# Commande pour afficher la liste de mots interdits
@commands.command(name="liste_mots_interdits")
async def list_banned_words(ctx):
    await ctx.send("Liste des mots interdits : " + ", ".join(banned_words))


# Commande pour supprimer un mot de la liste de mots interdits (réservée aux modérateurs)
@commands.command(name="supprimer_mot_interdit")
async def remove_banned_word(ctx, *words):
    if ctx.author.guild_permissions.administrator:
        words_removed = []
        words_not_in_list = []
        response = ""

        for word in words:
            if word in banned_words:
                banned_words.remove(word)
                words_removed.append(word)
            else:
                words_not_in_list.append(word)

        if words_removed:
            save_banned_words(banned_words)
            response = f"Mots supprimés de la liste des mots interdits : {', '.join(words_removed)}"

        if words_not_in_list:
            response += f"\nMots non présents dans la liste des mots interdits : {', '.join(words_not_in_list)}"

        if response:
            await ctx.send(response)
        else:
            await ctx.send("Aucun mot n'a été spécifié pour suppression.")

    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour supprimer un mot interdit."
        )


async def check_banned_word(message):
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
