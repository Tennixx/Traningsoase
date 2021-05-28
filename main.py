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
from discord import Guild




intents = discord.Intents.all()
bot = commands.Bot(command_prefix="to.", intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("TrainingsOase.net - System erfolgreich gestartet.")
    bot.loop.create_task(status_task())
    bot.ticket_configs = {}
    bot.reaction_roles = []

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
      lines = await file.readlines()
      for line in lines:
          data = line.split(" ")
          bot.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3]), int(data[4])]

async def status_task():
    while True:
      await bot.change_presence(status=discord.Status.dnd, activity=discord.Game('TraningsOase.net - System'))
      await asyncio.sleep(60)

@bot.event
async def on_raw_reaction_add(payload):
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(role_id))
            return

    if payload.member.id != bot.user.id and str(payload.emoji) == u"\U0001F3AB":
        msg_id, channel_id, category_id, role_id = bot.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = bot.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)

            ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
            ticket_channel = await category.create_text_channel(f"ticket {ticket_num}", topic=f"Supportticket von {payload.member.mention}", permission_synced=True)

            await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)
            await ticket_channel.set_permissions(guild.get_role(guild.id), send_messages=False,
                                                     read_messages=False)
            await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=True)

            message = await channel.fetch_message(msg_id)
            await message.remove_reaction(payload.emoji, payload.member)

            supporter = discord.utils.get(guild.roles, id=role_id)
            embed = discord.Embed(title=f"Ticket-System", description=f"Danke das du ein Ticket erstellt hast!\r\nBitte schildere dein Anligen so genau wie möglich, sodass dir geholfen werden kann.\r\n Benutze **'-close'** um das Ticket zu schließen.", color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
            embed.set_footer(icon_url=bot.user.avatar_url, text="Traningsoase.net - System")

            await ticket_channel.send(f"{payload.member.mention} | {supporter.mention} Willkommen im Ticket!")
            await ticket_channel.send(embed=embed)

            try:
                msg = await bot.wait_for("message", check=lambda m: m.channel == ticket_channel and m.content == "-claim_ticket", timeout=3600)

            except asyncio.TimeoutError:
                mbd = discord.Embed(title="Ticket claimed", description="{.author.mention} ist nun der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=False)
                await ticket_channel.set_permissions(guild.get_member(msg.author.id), read_messages=True, send_messages=True)
                await ticket_channel.send(embed=mbd)

            else:
                mbd1 = discord.Embed(title="Ticket claimed", description="{.author.mention} ist nun der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=False)
                await ticket_channel.set_permissions(guild.get_member(msg.author.id), read_messages=True, send_messages=True)
                await ticket_channel.send(embed=mbd1)

                try:
                    msg = await bot.wait_for("message", check=lambda m: m.channel == ticket_channel and m.content == "-unclaim_ticket", timeout=3600)

                except asyncio.TimeoutError:
                    mbd2 = discord.Embed(title="Ticket unclaimed", description="{.author.mention} ist nun nicht mehr der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                    await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=True)
                    await ticket_channel.send(embed=mbd2)

                else:
                    mbd3 = discord.Embed(title="Ticket unclaimed", description="{.author.mention} ist nun nicht mehr der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                    await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=True)
                    await ticket_channel.send(embed=mbd3)
                
                    try:
                        msg = await bot.wait_for("message", check=lambda m: m.channel == ticket_channel and m.content == "-claim_ticket", timeout=3600)

                    except asyncio.TimeoutError:
                        mbd4 = discord.Embed(title="Ticket claimed", description="{.author.mention} ist nun der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                        await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=False)
                        await ticket_channel.set_permissions(guild.get_member(msg.author.id), read_messages=True, send_messages=True)
                        await ticket_channel.send(embed=mbd4)

                    else:
                        mbd5 = discord.Embed(title="Ticket claimed", description="{.author.mention} ist nun der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                        await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=False)
                        await ticket_channel.set_permissions(guild.get_member(msg.author.id), read_messages=True, send_messages=True)
                        await ticket_channel.send(embed=mbd5)

                        try:
                            msg = await bot.wait_for("message", check=lambda m: m.channel == ticket_channel and m.content == "-unclaim_ticket", timeout=3600)

                        except asyncio.TimeoutError:
                            mbd6 = discord.Embed(title="Ticket claimed", description="{.author.mention} ist nun nicht mehr der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                            await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=True)
                            await ticket_channel.send(embed=mbd6)

                        else:
                            mbd7 = discord.Embed(title="Ticket claimed", description="{.author.mention} ist nun nicht mehr der Bearbeiter des Tickets.".format(msg), color=0x72C3EE)
                            await ticket_channel.set_permissions(guild.get_role(role_id), read_messages=True, send_messages=True)
                            await ticket_channel.send(embed=mbd7)


@bot.command()
@commands.has_permissions(manage_guild = True)
async def ticket(ctx , *, Message=None):
    embed = discord.Embed(title=f"Ticket-System", description=f"{Message}", color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
    embed.set_footer(icon_url=bot.user.avatar_url, text="Traningsoase.net - System")

    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_guild = True)
async def setupticket(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None, role: discord.Role=None):
    if msg is None or category is None or role is None:
        await ctx.channel.send("Fehler beim Konfigurieren des Tickets, ein Argument wurde nicht angegeben oder war ungültig.")
        return

    bot.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id, role.id] # this resets the configuration

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("ticket_configs.txt", mode="w") as file:
        await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id} {role.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)
                

    await msg.add_reaction(u"\U0001F3AB")
    embed = discord.Embed(title=":white_check_mark: Erfolgreich!", description=f"Das Ticketsystem wurde erfolgreich konfiguriert!", color=0x13FF00)
    embed.set_footer(text="Diese Nachricht wird in 5 Sekunden gelöscht!")
    await ctx.channel.send(embed=embed, delete_after=5)

Role1 = 841673827234742324

@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, id=Role1)
    await member.add_roles(role)
    print(f"{member} given {role}")



@bot.command()
async def save_ticket(ctx):
    async with ctx.typing():
        await ctx.message.delete()
        guild_id = bot.get_guild(773159030670753793)
        channel = bot.get_channel(847137867389206533)
        filename = "ticket.txt"
        with open(filename, "w") as file:
            async for msg in ctx.channel.history(limit=None, oldest_first=True):
                file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.content}\n")
            await asyncio.sleep(10)
    await channel.send(f"Ticket saved by {ctx.message.author.mention}")
    await channel.send(file=discord.File(filename))

@bot.command()
async def close_ticket(ctx):
    await ctx.message.delete()
    embed = discord.Embed(description="Das Ticket wurde geschlossen. Bewerte doch gerne unseren Support mit 1-5 Sternen. Solltest du dies **nicht** innerhalb von 24 Stunden tun, wird dieses Ticket gelöscht.", color=0x72C3EE)
    embed.set_footer(icon_url=bot.user.avatar_url, text="Traningsoase.net - System")
    await ctx.send(embed=embed)
    await asyncio.sleep(86400)
    await ctx.channel.delete()



bot.load_extension("cogs.general")
bot.run("...")
