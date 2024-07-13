import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# get private variables from .env file
load_dotenv()
token = os.getenv('TOKEN')
url = os.getenv('WEATHER_API_URL')
latitude = os.getenv('LATITUDE')
longitude = os.getenv('LONGITUDE')
wind_thresholds = os.getenv('WIND_THRESHOLDS')
global days
days = os.getenv('DAYS')

# set up intents
intents = discord.Intents.default()
intents.message_content = True

# create bot
bot = commands.Bot(command_prefix='!', intents=intents)

# sends a message when bot is ready
@bot.event
async def on_ready():
    print("Successfully logged in")

# remove the built-in help command to write own
bot.remove_command('help')
# lists all commands of the bot
@bot.command()
async def help(ctx):
    help_message = """\
    __**List of Commands:**__ :badminton:
**!winds <# of days>:** Displays wind speeds from 8 am to 8 pm, and distinguishes how suitable each hour is for play or not. Rain and other precipitation also have a significant impact.
**!key:** Shows a key that describes the levels of playability given the wind speed and precipitation.
*Note:* The <# of days> argument is optional and is limited from 1-16. If no number is provided, 3 is the default.
"""
    await ctx.send(help_message)

# uses the Open-Meteo API to gather wind data and displays 
@bot.command()
async def winds(ctx, arg: int = days):
    # checks if the argument, if there is one, is between 1 and 16
    if arg:
        days = int(arg)
        if days < 1 or days > 16:
            await ctx.send('The number of days must be between 1 and 16.')
            return
    
    await ctx.send(f"test{days}")

# displays key that describes how different wind speeds may affect play
@bot.command()
async def key(ctx):
    key_message = """\
:green_square:: Wind speed of 0-5 mph. Little to no issues.
:yellow_square:: Wind speed of 5-10 mph. Should not be too difficult to play, and a wind resistant shuttlecock will work well.
:orange_square:: Wind speed of 10-15 mph. Using a wind resistant shuttlecock is highly recommended.
:red_square:: Wind speed of 15+ mph and/or >10% chance of precipitation. Very poor conditions for outdoor badminton :smiling_face_with_tear:
"""
    await ctx.send(key_message)

# runs bot
bot.run(token)