import os
import discord
from discord.ext import commands, tasks
import time
import asyncio
from keep_alive import keep_alive

# Your channel ID
cid = 1148294754287767612
TOKEN = os.getenv("TOKEN")

# List of messages to send in order
messages = [

  '# Your texts here. ',
]

client = commands.Bot(command_prefix='$@#')

client._skip_check = lambda x, y: False

# Initialize an index to keep track of the current message
current_message_index = 0

@tasks.loop(seconds=9)
async def spammer():
    global current_message_index  # Access the global index

    text_channel = client.get_channel(cid)

    if text_channel is not None:
        try:
            # Send the current message and increment the index
            await text_channel.send(messages[current_message_index])
            current_message_index = (current_message_index + 1) % len(messages)  # Loop back to the start if at the end
            await asyncio.sleep(6)
        except discord.errors.Forbidden:
            print("403 Forbidden error occurred, but continuing...")
        except Exception as e:
            print(f"An error occurred in spammer loop: {e}")
            await asyncio.sleep(4)  # Wait for a moment before trying again

@tasks.loop(seconds=14400)
async def sleeper():
    await asyncio.sleep(3600)
    spammer.start()

spammer.start()

@client.command()
async def stop(ctx):
    spammer.stop()

@client.command()
async def spam(ctx):
    spammer.start()

keep_alive()
client.run(TOKEN, bot=False)
