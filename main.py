import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
USER_ID = int(os.getenv('USER_ID'))
HOME_CHANNEL_ID = int(os.getenv('HOME_CHANNEL_ID'))

# Validate that env variables are loaded correctly
if TOKEN is None or GUILD_ID is None or USER_ID is None or HOME_CHANNEL_ID is None:
    print("Failed to load env variables!")
    exit(0)

intents = discord.Intents().all()
client = discord.Client(intents=intents)


async def move_bot_to_channel(channel_name):
    """ Move the CrossPlatformBot to the specified voice channel """
    guild = client.get_guild(GUILD_ID)

    channel = discord.utils.get(guild.voice_channels, name=channel_name)
    if channel is None:
        print(f'Cannot move user: Invalid Channel {channel_name}')
        return None

    member = guild.get_member(USER_ID)
    if member is None:
        print("Cannot move user: Invalid User ID " + repr(USER_ID))
        return None

    try:
        await member.edit(voice_channel=channel)
        print(f'Moved user to channel {channel_name} ({repr(channel.id)})')
    except discord.errors.HTTPException:
        print("Voice bot is not connected to a voice channel.")

    #await channel.connect()


async def move_bot_to_home_channel():
    """Move the CrossPlatformBot to it's home channel"""
    guild = client.get_guild(GUILD_ID)

    channel = client.get_channel(HOME_CHANNEL_ID)
    if channel is None:
        print("Cannot move user: Invalid Channel ID")
        return None

    member = guild.get_member(USER_ID)
    if member is None:
        print("Cannot move user: Invalid User ID " + repr(USER_ID))
        return None

    try:
        await member.edit(voice_channel=channel)
        print(f'Moved user to home channel Home ({repr(channel.id)})')
    except discord.errors.HTTPException:
        print("Voice bot is not connected to a voice channel.")


@client.event
async def on_message(message):
    """Handle DM commands"""
    if message.author == client.user:
        return
    if message.content[0] == "!":
        if message.content == "!Home":
            await move_bot_to_home_channel()
        else:
            await move_bot_to_channel(message.content[1:])

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await move_bot_to_home_channel()

client.run(TOKEN)
