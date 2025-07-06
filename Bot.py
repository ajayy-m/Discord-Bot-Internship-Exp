import random                 # Necessary Imports
import discord
from discord.ext import commands

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
    jokes = [
    "Why do Java developers wear glasses? Because they don't see sharp.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "How does a penguin build its house? Igloos it together.",
    "Why was the math book sad? Because it had too many problems.",
    "I asked the librarian if the library had books on paranoia... she whispered, 'They're right behind you.'",
    "What do you call 8 hobbits? A hobbyte.",
    "What do you get if you cross a cat with a dark horse? Kitty Perry.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my computer I needed a break, and now it won’t stop sending me KitKats.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Why can't your nose be 12 inches long? Because then it would be a foot.",
    "What do you call a fish wearing a bowtie? Sofishticated.",
    "Why did the programmer quit his job? Because he didn’t get arrays.",
    "Why did the chicken join a band? Because it had the drumsticks.",
    "How do you comfort a JavaScript bug? You console it.",
    "Why did the cookie go to the hospital? Because it felt crummy.",
    "How do you organize a space party? You planet.",
    "Why don’t oysters donate to charity? Because they are shellfish.",
    "Why do cows wear bells? Because their horns don’t work.",
    "Why did the coffee file a police report? It got mugged.",
    "Why don’t some couples go to the gym? Because some relationships don’t work out."
]
    await ctx.send(random.choice(jokes))
# Command /Roll : Rolls a Die and gives you a number range between 1-6
@bot.command()
async def roll(ctx):
    await ctx.send(f"You rolled a 🎲 {random.randint(1, 6)}!")

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
