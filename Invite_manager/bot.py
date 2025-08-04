import discord
from discord.ext import commands
from db import add_invite, get_leaderboard, get_user_invite_count, clear_invites

TOKEN = "replace_this"  # Replace with your actual bot token

intents = discord.Intents.default()
intents.members = True
intents.invites = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
invites_cache = {}

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    for guild in bot.guilds:
        invites_cache[guild.id] = await guild.invites()

@bot.event
async def on_member_join(member):
    guild = member.guild
    after_invites = await guild.invites()
    before_invites = invites_cache.get(guild.id, [])

    for invite in after_invites:
        old = next((i for i in before_invites if i.code == invite.code), None)
        if old and invite.uses > old.uses:
            add_invite(guild.id, invite.inviter.id, member.id)
            break

    invites_cache[guild.id] = after_invites

@bot.command()
async def leaderboard(ctx):
    data = get_leaderboard(ctx.guild.id)
    if not data:
        await ctx.send("No invites yet.")
        return

    msg = "**🏆 Invite Leaderboard 🏆**\n"
    for idx, (user_id, count) in enumerate(data, 1):
        user = ctx.guild.get_member(int(user_id))
        name = user.name if user else f"<@{user_id}>"
        msg += f"{idx}. {name} - {count} invites\n"
    await ctx.send(msg)

@bot.command()
async def invites(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    count = get_user_invite_count(ctx.guild.id, member.id)
    await ctx.send(f"📨 {member.name} has invited **{count}** member(s) to this server.")

@bot.command()
@commands.has_permissions(administrator=True)
async def clearinvites(ctx, member: discord.Member = None):
    if member:
        clear_invites(ctx.guild.id, member.id)
        await ctx.send(f"✅ Cleared invites for {member.mention}.")
    else:
        clear_invites(ctx.guild.id)
        await ctx.send("🧹 All invites in this server have been cleared.")

bot.run(TOKEN)
