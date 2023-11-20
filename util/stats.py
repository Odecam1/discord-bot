from discord import Guild, Member, Status
from discord.ext import commands


@commands.command(name="stats")
async def server_info(ctx: commands.Context) -> None:
    server: Guild = ctx.guild
    total_members: int = len(server.members)
    total_bots: int = sum(1 for member in server.members if member.bot)
    online_members: int = sum(
        1 for member in server.members if member.status != Status.offline
    )

    total_channels: int = sum(
        1
        for channel in server.channels
        if not isinstance(channel, discord.CategoryChannel)
    )

    response: str = (
        f"Sur le serveur {server.name} :\n"
        f":busts_in_silhouette: Nombre de membres : {total_members} (y compris {total_bots} bots)\n"
        f":hash: Nombre de salons : {total_channels}\n"
        f":green_circle: Nombre de membres en ligne : {online_members}"
    )
    await ctx.send(response)
