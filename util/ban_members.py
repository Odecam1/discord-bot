from discord import Member
from discord.ext import commands
from typing import Optional


@commands.command(name="bannissement_membre")
async def ban_user(
    ctx: commands.Context,
    user: Member,
    *,
    reason: Optional[str] = "Aucune raison spécifiée",
) -> None:
    if ctx.author.guild_permissions.administrator:
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} a été banni pour la raison suivante : {reason}")
    else:
        await ctx.send(
            "Vous n'avez pas les autorisations nécessaires pour bannir un utilisateur."
        )
