import discord
from discord.ext import commands


@commands.command(name="stats")
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
