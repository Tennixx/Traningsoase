import discord
from discord import Message, Guild, TextChannel
from discord.ext import commands
from discord.utils import get 
from datetime import datetime 
import datetime
import asyncio
import random
import json
import aiofiles
import youtube_dl
import os
import pytz
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import aiosqlite
import math
import time

class help(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="TraningsOase.net - Hilfefenster", description="Hier seht ihr eine Liste aller Commands.", color=0x72C3EE)
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.set_footer(text="TraningsOase.net - System")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount=5):
        embed = discord.Embed(
            title=f":white_check_mark: Erfolgreich!",
            description=f"`{amount}` Nachricht/en wurden erfolgreich gelöscht!",
            color=0x13FF00
        )
        embed.set_footer(text="TraningsOase.net - System")
        await ctx.channel.purge(limit=amount+1)
        await asyncio.sleep(0.5)
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=embed, delete_after=7)

def setup(bot):
    bot.add_cog(help(bot))
    print("GENERAL is loaded!")
