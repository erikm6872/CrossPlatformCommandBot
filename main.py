import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
USER_ID = os.getenv('USER_ID')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

if TOKEN is None or USER_ID is None or CHANNEL_ID is None:
    print("Failed to load env variables!")
    exit(0)

client = discord.Client()
guild = client.get_guild(GUILD_ID)
print(guild)
print(guild.id)


async def move_user_to_channel():
    channel = client.get_channel(CHANNEL_ID)
    # channel now holds the channel you want to move people into
    if channel is None:
        print("Cannot move user: Invalid Channel ID")
        return None

    member = guild.get_member(USER_ID)    #commands.converter.MemberConverter().convert(guild, USER_ID)
    #member = client.get_user(767550258820677642)   #USER_ID)
    # member now holds the user that you want to move
    if member is None:
        print("Cannot move user: Invalid User ID")
        return None

    #await member.
    await member.edit(voice_channel=channel)
    #await channel.connect()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await move_user_to_channel()

client.run(TOKEN)
