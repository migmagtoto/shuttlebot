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
**!winds <# of days>:** Displays wind speeds from 6 am to 9 pm, and distinguishes how suitable each hour is for play or not. Rain and other precipitation also have a significant impact.
**!key:** Shows a key that describes the levels of playability given the wind speed and precipitation.
*Note:* The <# of days> argument is optional and is limited from 1-12. If no number is provided, 3 is the default.
"""
    await ctx.send(help_message)

# uses the Open-Meteo API to gather wind data and displays 
@bot.command()
async def winds(ctx, arg: int = days):
    # checks if the argument, if there is one, is between 1 and 16
    if arg:
        days = int(arg)
        if days < 1 or days > 12:
            await ctx.send('The number of days must be between 1 and 12.')
            return
        
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=precipitation_probability,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FNew_York&forecast_days={days}'
    response = requests.get(url)
    data = response.json()
    weather_data = data['hourly']

    end_time = datetime.now() + timedelta(days=days)

    #forecast_message = f'Playability of the next {days} days:\n'
    forecast_message = ""

    for i in range(len(weather_data['time'])):
        timestamp = weather_data['time'][i]
        hour_time = datetime.fromisoformat(timestamp)

        if hour_time > end_time:
            break

        if hour_time.hour == 8:
            forecast_message += f'{hour_time.strftime('%a %m/%d')}\n'

        if 18 <= hour_time.hour <= 21: # between 6-9 pm
            wind_speed = weather_data['wind_speed_10m'][i]
            precipitation = weather_data['precipitation_probability'][i]

            if precipitation > 30 or wind_speed > 15:
                forecast_message += f':red_square: {hour_time.strftime('%I %p').lstrip('0').lower()}: {wind_speed} mph, {precipitation}%\n'
            elif precipitation > 20 or wind_speed > 10:
                forecast_message += f':orange_square: {hour_time.strftime('%I %p').lstrip('0').lower()}: {wind_speed} mph, {precipitation}%\n'
            elif wind_speed > 5:
                forecast_message += f':yellow_square: {hour_time.strftime('%I %p').lstrip('0').lower()}: {wind_speed} mph, {precipitation}%\n'
            else:
                forecast_message += f':green_square: {hour_time.strftime('%I %p').lstrip('0').lower()}: {wind_speed} mph, {precipitation}%\n'

    await ctx.send(forecast_message)

# displays key that describes how different wind speeds may affect play
@bot.command()
async def key(ctx):
    key_message = """\
:green_square:: Wind speed of 0-5 mph. Little to no issues.
:yellow_square:: Wind speed of 5-10 mph. Should not be too difficult to play, and a wind resistant shuttlecock will work well.
:orange_square:: Wind speed of 10-15 mph and/or >20% chance of precipitation. Using a wind resistant shuttlecock is recommended.
:red_square:: Wind speed of 15+ mph and/or >30% chance of precipitation. Very poor conditions for outdoor badminton :smiling_face_with_tear:
"""
    await ctx.send(key_message)

# runs bot
bot.run(token)