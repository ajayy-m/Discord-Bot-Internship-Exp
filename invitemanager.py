import discord #Necessary imports
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Needed to track members joining
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Dictionary to track invites per guild
invite_cache = {}

@bot.event             #
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    for guild in bot.guilds:
        invites = await guild.invites()
        invite_cache[guild.id] = {invite.code: invite.uses for invite in invites}

@bot.event
async def on_member_join(member):                
    guild = member.guild
    new_invites = await guild.invites()
    old_invites = invite_cache[guild.id]

    for invite in new_invites:
        if invite.code in old_invites:
            if invite.uses > old_invites[invite.code]:
                inviter = invite.inviter
                await guild.system_channel.send(
                    f"{member.mention} joined using {inviter.mention}'s invite! 🎉"
                )
                break
    # Update cache
    invite_cache[guild.id] = {invite.code: invite.uses for invite in new_invites}
  
@bot.command()        # Command - Check invites
async def invites(ctx, member: discord.Member = None):
    member = member or ctx.author
    total = 0
    invites = await ctx.guild.invites()
    for invite in invites:
        if invite.inviter == member:
            total += invite.uses
    await ctx.send(f"{member.mention} has invited **{total}** member(s) to the server.")

