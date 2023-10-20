from discord.ext import commands
from util.json_ban_word import save_banned_words, load_banned_words

banned_words = load_banned_words()


# Fonction pour ajouter ou supprimer un mot de la liste de mots interdits
async def update_banned_words(ctx, action, *words):
    if ctx.author.guild_permissions.administrator:
        words_changed = []
        words_not_changed = []
        response = ""

        for word in words:
            is_banned_word = word in banned_words

            if action == "ajouter" and not is_banned_word:
                banned_words.append(word)
            elif action == "supprimer" and is_banned_word:
                banned_words.remove(word)
            else:
                words_not_changed.append(word)
                continue
            words_changed.append(word)

        if words_changed:
            save_banned_words(banned_words)
            response = f"Mots {action[:-2]}és de la liste des mots interdits : {", ".join(words_changed)}"

        if words_not_changed:
            adverb = (
                "déjà" if action == "ajouter" else "non"
            )  # Changer "non" en fonction de l'action

            response += f"\nMots {adverb} présents dans la liste des mots interdits : {", ".join(words_not_changed)}"

        if response:
            await ctx.send(response)
        else:
            await ctx.send(f"Aucun mot n'a été spécifié pour {action}.")

    else:
        await ctx.send(
            f"Vous n'avez pas les autorisations nécessaires pour {action} un mot interdit."
        )


# Commande pour ajouter des mots à la liste de mots interdits (réservée aux modérateurs)
@commands.command(name="ajouter_mot_interdit")
async def add_banned_word(ctx, *words):
    await update_banned_words(ctx, "ajouter", *words)


# Commande pour supprimer un mot de la liste de mots interdits (réservée aux modérateurs)
@commands.command(name="supprimer_mot_interdit")
async def remove_banned_word(ctx, *words):
    await update_banned_words(ctx, "supprimer", *words)


# Commande pour afficher la liste de mots interdits
@commands.command(name="liste_mots_interdits")
async def list_banned_words(ctx):
    await ctx.send("Liste des mots interdits : " + ", ".join(banned_words))


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
