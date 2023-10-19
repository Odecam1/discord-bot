import discord
import random

CHANNEL_ID = ""

intents = discord.Intents.default()
intents.members = True
bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)


async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Salut {member.mention} ! Bienvenue sur le serveur.")


@bot.command()
async def server_info(ctx):
    server = ctx.guild
    total_members = len(server.members)
    online_members = sum(
        member.status == discord.Status.online for member in server.members
    )
    total_channels = len(server.channels)

    response = f"Nombre total de membres : {total_members}\nMembres en ligne : {online_members}\nNombre de canaux : {total_channels}"
    await ctx.send(response)


@bot.command()
async def create_poll(ctx, question, *options):
    poll_embed = discord.Embed(title=question)
    for option in options:
        poll_embed.add_field(name=option, value="0", inline=False)

    poll_message = await ctx.send(embed=poll_embed)

    for i in range(len(options)):
        await poll_message.add_reaction(f"{i+1}\u20e3")
