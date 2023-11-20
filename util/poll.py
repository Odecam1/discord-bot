from discord import Embed
from discord.ext import commands
from typing import Tuple


@commands.command(name="sondage")
async def create_poll(ctx: commands.Context, question: str, *options: str) -> None:
    poll_embed: Embed = Embed(title=question)
    for option in options:
        poll_embed.add_field(name=option, value="0", inline=False)

    poll_message = await ctx.send(embed=poll_embed)

    for i in range(len(options)):
        await poll_message.add_reaction(f"{i+1}\u20e3")
