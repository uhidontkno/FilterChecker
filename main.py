from discord.ext import commands
import discord
import re
from filters import *
import os
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None,intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.slash_command(name="check")
async def check(ctx, url):
    await ctx.defer()

    # Extract FQDN using regex
    fqdn_match = re.search(r'https?://([^/]+)', url)
    fqdn = fqdn_match.group(1) if fqdn_match else None

    if fqdn:
        embed = {
            'title': f"Results for {fqdn}",
            'description': f"FortiGuard: {await fortiguard(fqdn)}\nLightspeed: {await lightspeed(fqdn)}\nPalo Alto: {await pan(fqdn)}\nGoogle Safe Browsing: {'Dangerous' if await safe_browsing(fqdn) else 'Not Dangerous'}"
        }
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.respond("Invalid URL provided.",ephemeral=True)

bot.run(os.environ['BOT_TOKEN'])
