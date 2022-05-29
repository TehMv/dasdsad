
# Imports
import requests
import time
import discord
from discord.ext import commands

# Set Prefix
client = commands.Bot(command_prefix = '!')

# To send message with the bot (for the bot can to update the message)
@client.command()
@commands.has_permissions(administrator = True)
async def embed(ctx):
  await ctx.channel.purge(limit=1)
  embed = discord.Embed(
    colour = discord.Colour.blue(),
    title = f'Embed'
  )
  await ctx.send(embed=embed)

# Setting variables **U need change this**
TOKEN = ''
IP = '195.133.95.17:30120'
channel_id = 839518333396181234
message_id = 839518906346631234

# Send when the bot in online
@client.event
async def on_ready():
   print(f'Logged as {client.user.name}')
   client.loop.create_task(players())

# Update a message and status every minute
async def players():
  while True:
    channel = client.get_channel(channel_id)
    msg_id = message_id
    msg = await channel.fetch_message(msg_id)
    try:
      # Players Information
      x = requests.get(f'http://{IP}/players.json')
      info = x.json()
      # Server Information 
      p = requests.get(f'http://{IP}/dynamic.json')
      server = p.json()
      # maxPlayers & Players
      players, maxPlayers = server['clients'], server['sv_maxclients']
      # Players list 
      playernames = ''
      for player in info:
        playernames += f"[{player['id']}] {player['name']}"

        for info in player['identifiers']:
          if 'discord' in info:
            playernames += f' <@{info[8:]}>\n'
             
      # Embed
      embed = discord.Embed(
        colour = discord.Colour.blue(),
        title = f'Status: {players}/{maxPlayers}',
        description= playernames
      )
      await msg.edit(embed=embed)
      await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'🐌({players}/{maxPlayers})'))
    except:
      embed = discord.Embed(
        colour = discord.Colour.blue(),
        title = f'Status: Offline',
      )
      await msg.edit(embed=embed)
      await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'🐌(Offline))'))

    # Update every minute (60 seconds)
    time.sleep(60)

# Run the bot
client.run(TOKEN)
