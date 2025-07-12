import random                 # Necessary Imports
import discord
from discord.ext import commands
import aiohttp

intents = discord.Intents.default()
intents.message_content = True
# Giving a Bot Prefix
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f" Logged in as {bot.user}")

# Command /joke :sends a random joke from a predefined list

@bot.command()
async def joke(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://official-joke-api.appspot.com/random_joke") as response:
            if response.status == 200:
                data = await response.json()
                joke_text = f"{data['setup']} {data['punchline']}"
                await ctx.send(joke_text)
            else:
                await ctx.send("Couldn't fetch a joke at the moment. Try again later!")

# Command /eightball : Gives a predefined set of answers for an asked Question
@bot.command()
async def eightball(ctx, *, question):
    responses = [
        "Yes.", "No.", "Maybe.", "Definitely!", "I don't think so.",
        "Ask again later.", "Absolutely!", "Not in a million years."
    ]
    await ctx.send(f"🎱 {random.choice(responses)}")

# Command /Choose : Randomly pick a choice out of many give choices
@bot.command()
async def choose(ctx, *choices):
    if not choices:
        await ctx.send("Give me some choices to pick from!")
    else:
        await ctx.send(f"I choose: **{random.choice(choices)}**")

bot.run("Token")
