import os
import time
import random
import sqlite3
import discord
from discord import app_commands

TOKEN = os.getenv("bot_token")
BOT_NAME = "My First Bot"
START_TIME = time.time()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

db = sqlite3.connect("bot.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER DEFAULT 0,
    last_daily INTEGER DEFAULT 0
)
""")
db.commit()

def make_embed(title=None, description=None, color=discord.Color.blurple()):
    return discord.Embed(title=title, description=description, color=color)

def ensure_user(user_id: int):
    cursor.execute("SELECT coins, last_daily FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            "INSERT INTO users (user_id, coins, last_daily) VALUES (?, 0, 0)",
            (user_id,)
        )
        db.commit()
        return 0, 0

    return row

async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Game(name="/help"))
    print(f"{BOT_NAME} online as {client.user}")

client.add_listener(on_ready, "on_ready")

async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        embed=make_embed(
            "Pong",
            f"Latency: {round(client.latency * 1000)}ms"
        )
    )

tree.add_command(app_commands.Command(
    name="ping",
    description="Check bot latency",
    callback=ping
))

async def uptime(interaction: discord.Interaction):
    elapsed = int(time.time() - START_TIME)
    h, rem = divmod(elapsed, 3600)
    m, s = divmod(rem, 60)

    await interaction.response.send_message(
        embed=make_embed(
            "Uptime",
            f"{h}h {m}m {s}s"
        )
    )

tree.add_command(app_commands.Command(
    name="uptime",
    description="Check bot uptime",
    callback=uptime
))

async def balance(interaction: discord.Interaction):
    coins, _ = ensure_user(interaction.user.id)

    await interaction.response.send_message(
        embed=make_embed(
            "Balance",
            f"You have **{coins}** coins."
        )
    )

tree.add_command(app_commands.Command(
    name="balance",
    description="Check your balance",
    callback=balance
))

async def daily(interaction: discord.Interaction):
    coins, last = ensure_user(interaction.user.id)
    now = int(time.time())

    if now - last < 86400:
        remaining = 86400 - (now - last)
        h = remaining // 3600
        m = (remaining % 3600) // 60

        await interaction.response.send_message(
            embed=make_embed(
                "Daily Reward",
                f"Come back in {h}h {m}m."
            ),
            ephemeral=True
        )
        return

    reward = random.randint(100, 250)
    cursor.execute(
        "UPDATE users SET coins = coins + ?, last_daily = ? WHERE user_id = ?",
        (reward, now, interaction.user.id)
    )
    db.commit()

    await interaction.response.send_message(
        embed=make_embed(
            "Daily Reward",
            f"You received **{reward}** coins."
        )
    )

tree.add_command(app_commands.Command(
    name="daily",
    description="Claim your daily reward",
    callback=daily
))

async def flip(interaction: discord.Interaction):
    await interaction.response.send_message(
        embed=make_embed(
            "Coin Flip",
            random.choice(["Heads", "Tails"])
        )
    )

tree.add_command(app_commands.Command(
    name="flip",
    description="Flip a coin",
    callback=flip
))

async def roll(interaction: discord.Interaction, dice: str):
    try:
        rolls, limit = map(int, dice.lower().split("d"))
        if rolls > 20 or limit > 1000:
            raise ValueError
    except ValueError:
        await interaction.response.send_message(
            embed=make_embed(
                "Invalid Format",
                "Use NdN format (example: 2d6).",
                discord.Color.orange()
            ),
            ephemeral=True
        )
        return

    results = [random.randint(1, limit) for _ in range(rolls)]
    await interaction.response.send_message(
        embed=make_embed(
            "Dice Roll",
            f"{' + '.join(map(str, results))} = **{sum(results)}**"
        )
    )

tree.add_command(app_commands.Command(
    name="roll",
    description="Roll dice (NdN format)",
    callback=roll
))

async def help_cmd(interaction: discord.Interaction):
    e = make_embed("Help Menu")
    e.add_field(name="Utility", value="ping, uptime", inline=False)
    e.add_field(name="Economy", value="balance, daily", inline=False)
    e.add_field(name="Fun", value="flip, roll", inline=False)

    await interaction.response.send_message(embed=e)

tree.add_command(app_commands.Command(
    name="help",
    description="Show bot commands",
    callback=help_cmd
))

client.run(TOKEN)
