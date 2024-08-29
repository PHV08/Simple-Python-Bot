import discord
import os
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

# Global variables
token = os.getenv("bot_token")
bot_name = "My First Bot"
cmd_prefix = "|"

# Initialize bot
client = commands.Bot(command_prefix=cmd_prefix, intents=discord.Intents.all())
client.remove_command('help')

# Bot ready event
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{cmd_prefix}help"))
    print(f"{bot_name} is online and ready!")

# Utility Commands
@client.command()
async def ping(ctx):
    """Check the bot's latency."""
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def uptime(ctx):
    """Check bot uptime."""
    await ctx.send("Bot has been running smoothly!")

@client.command()
async def serverinfo(ctx):
    """Displays information about the server."""
    server = ctx.guild
    num_text_channels = len(server.text_channels)
    num_voice_channels = len(server.voice_channels)
    num_roles = len(server.roles)
    num_members = server.member_count

    embed = discord.Embed(title=f"Server Info: {server.name}", color=discord.Color.blue())
    embed.add_field(name="Text Channels", value=num_text_channels)
    embed.add_field(name="Voice Channels", value=num_voice_channels)
    embed.add_field(name="Roles", value=num_roles)
    embed.add_field(name="Members", value=num_members)
    await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx, member: discord.Member = None):
    """Displays information about a user."""
    member = member or ctx.author
    roles = [role.name for role in member.roles[1:]]  # Exclude @everyone role
    embed = discord.Embed(title=f"User Info: {member}", color=discord.Color.green())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Roles", value=", ".join(roles))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

# Moderation Commands
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    """Clear messages in a channel."""
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Cleared {amount} messages!", delete_after=5)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a user from the server."""
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked for {reason}.")

# Fun Commands
@client.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    import random
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@client.command()
async def flip(ctx):
    """Flips a coin."""
    import random
    result = random.choice(["Heads", "Tails"])
    await ctx.send(result)

@client.command()
async def joke(ctx):
    """Tell a random joke."""
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    await ctx.send(random.choice(jokes))

# Information Command
@client.command()
async def botinfo(ctx):
    """Displays information about the bot."""
    embed = discord.Embed(title=f"{bot_name} Info", description="A multipurpose Discord bot!", color=discord.Color.purple())
    embed.add_field(name="Author", value="Unknown")
    embed.add_field(name="Library", value="discord.py")
    embed.add_field(name="Prefix", value=cmd_prefix)
    await ctx.send(embed=embed)

# Error Handling
@suggest.error
async def suggest_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        em = discord.Embed(title="Slow down!", description=f"Try again in {error.retry_after:.2f} seconds.", color=discord.Color.red())
        await ctx.send(embed=em)

# Help Command
@client.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description="Available commands are listed below.", color=discord.Color.orange())
    embed.add_field(name="Utility Commands", value="`ping`, `uptime`, `serverinfo`, `userinfo`", inline=False)
    embed.add_field(name="Moderation Commands", value="`clear`, `kick`", inline=False)
    embed.add_field(name="Fun Commands", value="`roll`, `flip`, `joke`", inline=False)
    embed.add_field(name="Information Commands", value="`botinfo`", inline=False)
    await ctx.send(embed=embed)

# Run the bot
client.run(token)
