import discord
from discord.ext import commands
import aiohttp

# API keys - weatherapi~
WEATHER_API_KEY = "Enter_Weatherapi"
BASE_URL = "http://api.weatherapi.com/v1"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)  # Disable default help

# Fetch Weather 
async def get_weather(city):
    url = f"{BASE_URL}/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "aqi": "no"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

#Fetch Forecast 
async def get_forecast(city):
    url = f"{BASE_URL}/forecast.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "days": 3,
        "aqi": "no",
        "alerts": "no"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

# /city <city_name> : Provides the Weather of the city at present time
@bot.command()
async def city(ctx, *, city: str):
    data = await get_weather(city)
    if not data:
        await ctx.send("❌ Couldn't fetch weather for that city.")
        return

    location = data["location"]
    current = data["current"]
    condition = current["condition"]["text"]

    embed = discord.Embed(
        title=f"🌤 Current Weather: {location['name']}, {location['country']}",
        description=f"{condition}",
        color=discord.Color.green()
    )
    embed.add_field(name="🌡 Temperature", value=f"{current['temp_c']}°C", inline=True)
    embed.add_field(name="💨 Wind", value=f"{current['wind_kph']} kph", inline=True)
    embed.add_field(name="🕒 Local Time", value=location['localtime'], inline=False)
    await ctx.send(embed=embed)

# /forecast <city_name> Provides forecast of a city of the next 3 days
@bot.command()
async def forecast(ctx, *, city: str):
    data = await get_forecast(city)
    if not data:
        await ctx.send("❌ Couldn't fetch forecast.")
        return

    location = data["location"]
    forecast_days = data["forecast"]["forecastday"]

    embed = discord.Embed(
        title=f"📅 3-Day Forecast: {location['name']}, {location['country']}",
        color=discord.Color.green()
    )

    for day in forecast_days:
        date = day["date"]
        condition = day["day"]["condition"]["text"]
        max_temp = day["day"]["maxtemp_c"]
        min_temp = day["day"]["mintemp_c"]
        rain_chance = day["day"]["daily_chance_of_rain"]
        embed.add_field(
            name=f"{date}",
            value=f"{condition}\n🌡 {min_temp}°C ~ {max_temp}°C\n☔ Rain Chance: {rain_chance}%",
            inline=False
        )
    await ctx.send(embed=embed)

# /help - Provides the list of commands used by the bot, AJutils!!! 
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📘 Help - List of Commands for AJUtils",
        color=discord.Color.green()
    )
    embed.add_field(
        name="/city   <city_name>",
        value="Shows the current weather of the specified city.",
        inline=False
    )
    embed.add_field(
        name="/forecast  <city_name>",
        value="Displays weather forecast of the city on the next 3 days.",
        inline=False
    )
    await ctx.send(embed=embed)

# Bot token
bot.run("Enter Bot Token")
