import discord
from discord.ext import commands


@commands.command(name="bannisement_membre")
async def ban_user(ctx, user: discord.user, *, reason="Aucune raison spécifiée"):
    if ctx.author.guild_permissions.administrator:
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} a été banni pour la raison suivante : {reason}")
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour bannir un utilisateur."
        )