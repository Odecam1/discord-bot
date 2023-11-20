from discord.ext import commands
from discord import Member, Message, TextChannel, Intents
from util.stats import server_info
from util.banned_words import (
    add_banned_words,
    list_banned_words,
    remove_banned_words,
    check_banned_word,
)
from util.clean import clear
from util.poll import create_poll
from util.ban_members import ban_user
from typing import List, Union

channel_id_member_join: int = 1164540231484198952
token: str = "MTE2NDUyNjI1MTAzODQ3NDMxMA.GqT52w.LBoVE9d-Uu4uzwJfH3HfvVq5zyTxX09B7Sv1EI"

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} est prêt")


@bot.event
async def on_member_join(member: Member) -> None:
    channel: TextChannel = bot.get_channel(channel_id_member_join)
    await channel.send(f"Salut {member.mention} ! Bienvenue sur le serveur.")


@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    await check_banned_word(message)
    await bot.process_commands(message)


commands_list: List[commands.Command] = [
    server_info,
    add_banned_words,
    remove_banned_words,
    list_banned_words,
    clear,
    create_poll,
    ban_user,
]

for command in commands_list:
    bot.add_command(command)

bot.run(token)
