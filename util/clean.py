from discord.ext import commands


@commands.Bot.command()
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
