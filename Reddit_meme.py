import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# List of subreddits 
SUBREDDITS = ["memes", "dankmemes", "wholesomememes", "funny", "me_irl"]

autopost_tasks = {}

#Meme Fetcher Function
async def fetch_meme():
    subreddit = random.choice(SUBREDDITS)
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"

    headers = {"User-Agent": "DiscordMemeBot"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return None

            data = await resp.json()
            posts = data["data"]["children"]
            memes = [post["data"] for post in posts if not post["data"]["over_18"] and post["data"].get("post_hint") == "image"]
            if not memes:
                return None

            meme = random.choice(memes)
            return meme

# /meme - Fetches a meme directly from the given subreddits ( within the code )
@bot.command()
async def meme(ctx):
    meme = await fetch_meme()
    if not meme:
        await ctx.send("❌ Couldn't fetch a meme right now.")
        return

    embed = discord.Embed(
        title=meme['title'],
        url=f"https://reddit.com{meme['permalink']}",
        color=discord.Color.purple()
    )
    embed.set_image(url=meme['url'])
    embed.set_footer(text=f"👍 {meme['ups']} | 💬 {meme['num_comments']} | r/{meme['subreddit']}")
    await ctx.send(embed=embed)

# /autopost <channel_name> <time_in_seconds> : Autoposts meme every X seconds provided by the USer
@bot.command()
async def autopost(ctx, channel: discord.TextChannel, interval: int):
    if channel.id in autopost_tasks:
        await ctx.send(f"🔁 Auto-posting is already running in {channel.mention}.")
        return

    async def auto_send():
        await bot.wait_until_ready()
        while True:
            meme = await fetch_meme()
            if meme:
                embed = discord.Embed(
                    title=meme['title'],
                    url=f"https://reddit.com{meme['permalink']}",
                    color=discord.Color.green()
                )
                embed.set_image(url=meme['url'])
                embed.set_footer(text=f"👍 {meme['ups']} | 💬 {meme['num_comments']} | r/{meme['subreddit']}")
                await channel.send(embed=embed)
            await asyncio.sleep(interval)

    task = asyncio.create_task(auto_send())
    autopost_tasks[channel.id] = task
    await ctx.send(f"✅ Auto-posting memes to {channel.mention} every {interval} seconds.")

# /stopautopost - Stops the autoposting in a Channel
@bot.command()
async def stopautopost(ctx, channel: discord.TextChannel):
    task = autopost_tasks.pop(channel.id, None)
    if task:
        task.cancel()
        await ctx.send(f"🛑 Stopped auto-posting in {channel.mention}.")
    else:
        await ctx.send(f"❌ No auto-posting task running in {channel.mention}.")

# --- Run the Bot ---
bot.run("Enter_Bot_Token_From_Discord_Developer_Portal")
