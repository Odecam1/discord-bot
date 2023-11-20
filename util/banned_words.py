from discord import Message
from discord.ext import commands
from util.json_ban_word import save_banned_words, load_banned_words
from typing import List

banned_words: List[str] = load_banned_words()


def join_list(list_str: List[str]) -> str:
    return ", ".join(list_str)


async def update_banned_words(ctx: commands.Context, action: str, *words: str) -> None:
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(
            f"Vous n'avez pas les autorisations nécessaires pour {action} un mot interdit."
        )
        return

    words_changed: List[str] = []
    words_not_changed: List[str] = []
    response: str = ""
    is_add: bool = action == "ajouter"

    for word in words:
        is_banned_word = word in banned_words

        if is_add and not is_banned_word:
            banned_words.append(word)
        elif action == "supprimer" and is_banned_word:
            banned_words.remove(word)
        else:
            words_not_changed.append(word)
            continue
        words_changed.append(word)

    if words_changed:
        save_banned_words(banned_words)
        action_word = "à" if is_add else "de"
        response = f"Mots {action[:-2]}és {action_word} la liste des mots interdits : {join_list(words_changed)}"

    if words_not_changed:
        adverb = "déjà" if is_add else "non"
        response += f"\nMots {adverb} présents dans la liste des mots interdits : {join_list(words_not_changed)}"

    if response:
        await ctx.send(response)
    else:
        await ctx.send(f"Aucun mot n'a été spécifié pour {action}.")


@commands.command(name="ajouter_mots_interdit")
async def add_banned_words(ctx: commands.Context, *words: str) -> None:
    await update_banned_words(ctx, "ajouter", *words)


@commands.command(name="supprimer_mots_interdit")
async def remove_banned_words(ctx: commands.Context, *words: str) -> None:
    await update_banned_words(ctx, "supprimer", *words)


@commands.command(name="liste_mots_interdits")
async def list_banned_words(ctx: commands.Context) -> None:
    await ctx.send("Liste des mots interdits : " + join_list(banned_words))


async def check_banned_word(message: Message) -> None:
    message_content: str = message.content.lower()

    for banned_word in banned_words:
        if banned_word in message_content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, veuillez éviter d'utiliser des mots interdits."
            )
            break
