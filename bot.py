# Physics Brawl Mock Bot
# Delta0001
# Hosted on GitHub @ https://github.com/SuperSat001/Discord-Mock-Bot
# Fair use of code allowed

import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from math import ceil
from copy import deepcopy
from itertools import groupby

pres_range = 0.05 # range of acceptable answers

with open("pb2019/ans.txt") as f:
    r = []
    for k in f.readlines():
        r.append(k.strip())
    c = [list(group) for k, group in groupby(r, lambda x: x == "x") if not k]
    major_ans = [float(x) for x in c[0]]
    hm_ans = [float(x) for x in c[1]]
    he_ans = [float(x) for x in c[2]]
    hx_ans = [float(x) for x in c[3]]

with open("pb2019/pts.txt") as f:
    r = []
    for k in f.readlines():
        r.append(k.strip())
    c = [list(group) for k, group in groupby(r, lambda x: x == "x") if not k]
    major_points = [int(x) for x in c[0]]
    hm_points = [int(x) for x in c[1]]
    he_points = [int(x) for x in c[2]]
    hx_points = [int(x) for x in c[3]]


points_scored = {}
out_channel = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="?")


@bot.event
async def on_ready():
    global points_scored, out_channel
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="mock Physics Brawl"))
    for guild in bot.guilds:
        print(guild, guild.id)
        points_scored[guild.id] = 0
        out_channel[guild.id] = -1

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.command(name="usage", help="Usage Instructions")
async def test(ctx):
    await ctx.send(file=discord.File("readme.md"))


@bot.command(name="out", help="Set output channel")
@commands.has_role('mock')
async def out(ctx, num:int):
    global out_channel
    out_channel[ctx.message.guild.id] = num
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])
    await ctx.send(f"Output set to {out_channel[ctx.message.guild.id]}")
    await outChannel.send(f"Output set to {out_channel[ctx.message.guild.id]}")


@bot.command(name="add", help="Add bonous points")
@commands.has_role('mock')
async def add(ctx, num:int):
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])
    global points_scored
    points_scored[ctx.message.guild.id] += num
    await ctx.send(f"{num} points added")
    await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")


@bot.command(name="major", help="Start Major round")
@commands.has_role('mock')
async def major(ctx):

    global points_scored
    major_value = deepcopy(major_points)

    channel = ctx.message.channel

    if out_channel[ctx.message.guild.id] == -1:
        await ctx.send("Please set Output Channel")
        return False

    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = major_ans[i-1]
        return ((abs(ans-cor)/cor)<(pres_range/2))

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>1:
            return cur
        else:
            return 1

    await ctx.send("Asking Questions.....\nMajor")

    i = 1
    while i<=len(major_ans):

        qn = "pb2019/images/" + str(i) + ".PNG"
        await ctx.send(file=discord.File(qn))
        await ctx.send(f"{ceil(major_value[i-1])} points")        
	   
        msg = await bot.wait_for('message', check=check)

        if msg.content.lower() == "skip":
            await ctx.send("Skipped")
            points_scored[ctx.message.guild.id] -= 1
            await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
            i += 1
        elif msg.content.lower() == "exit":
            await ctx.send("Stopped")
            break
        elif msg.content.replace('.', '', 1).isdigit():
            r = float(msg.content)
            await ctx.send(f"Recorded answer is {r}")
            await outChannel.send(f"Major {i} = {r}")
            if validate(r, i):
                points_scored[ctx.message.guild.id] += ceil(major_value[i-1])
                await ctx.send(f"Correct, {ceil(major_value[i-1])} points awarded")
                await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
                i += 1
            else:
                major_value[i-1] = reduce(major_value[i-1], major_points[i-1])
                await ctx.send(f"Incorrect, question is now of {ceil(major_value[i-1])} points")
        else:
            await ctx.send("Invalid Answer") 

    await ctx.send("Major Complete")
    await outChannel.send("Major Complete")


@bot.command(name="hm", help="Start Hurry-Up Mechanics round")
@commands.has_role('mock')
async def hm(ctx):

    global points_scored
    hm_value = deepcopy(hm_points)

    channel = ctx.message.channel

    if out_channel[ctx.message.guild.id] == -1:
        await ctx.send("Please set Output Channel")
        return False

    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = hm_ans[i-1]
        return ((abs(ans-cor)/cor)<(pres_range/2))

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>0:
            return cur
        else:
            return 0

    await ctx.send("Asking Questions..... \nHurry-Up Mechanics")

    i = 1
    while i<=len(hm_ans):
        qn = "pb2019/images/m" + str(i) + ".PNG"
        await ctx.send(file=discord.File(qn))
        await ctx.send(f"{ceil(hm_value[i-1])} points")        
       
        msg = await bot.wait_for('message', check=check)

        if msg.content.lower() == "skip":
            await ctx.send("Skipped")
            points_scored[ctx.message.guild.id] -= 1
            await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
            i += 1
        elif msg.content.lower() == "exit":
            await ctx.send("Stopped")
            break
        elif msg.content.replace('.', '', 1).isdigit():
            r = float(msg.content)
            await ctx.send(f"Recorded answer is {r}")
            await outChannel.send(f"Hurry M {i} = {r}")
            if validate(r, i):
                points_scored[ctx.message.guild.id] += ceil(hm_value[i-1])
                await ctx.send(f"Correct, {ceil(hm_value[i-1])} points awarded")
                await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
                i += 1
            else:
                hm_value[i-1] = reduce(hm_value[i-1], hm_points[i-1])
                await ctx.send(f"Incorrect, question is now of {ceil(hm_value[i-1])} points")
        else:
            await ctx.send("Invalid Answer")

    await ctx.send("Hurry-Up Mechanics Complete")
    await outChannel.send("Hurry-Up Mechanics Complete")


@bot.command(name="he", help="Start Hurry-Up EM round")
@commands.has_role('mock')
async def he(ctx):

    global points_scored
    he_value = deepcopy(he_points)
    channel = ctx.message.channel

    if out_channel[ctx.message.guild.id] == -1:
        await ctx.send("Please set Output Channel")
        return False

    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = he_ans[i-1]
        return ((abs(ans-cor)/cor)<(pres_range/2))

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>0:
            return cur
        else:
            return 0

    await ctx.send("Asking Questions..... \nHurry-Up EM")

    i = 1
    while i<=len(he_ans):
        qn = "pb2019/images/e" + str(i) + ".PNG"
        await ctx.send(file=discord.File(qn))
        await ctx.send(f"{ceil(he_value[i-1])} points")        
       
        msg = await bot.wait_for('message', check=check)

        if msg.content.lower() == "skip":
            await ctx.send("Skipped")
            points_scored[ctx.message.guild.id] -= 1
            await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
            i += 1
        elif msg.content.lower() == "exit":
            await ctx.send("Stopped")
            break
        elif msg.content.replace('.', '', 1).isdigit():
            r = float(msg.content)
            await ctx.send(f"Recorded answer is {r}")
            await outChannel.send(f"Hurry E {i} = {r}")
            if validate(r, i):
                points_scored[ctx.message.guild.id] += ceil(he_value[i-1])
                await ctx.send(f"Correct, {ceil(he_value[i-1])} points awarded")
                await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
                i += 1
            else:
                he_value[i-1] = reduce(he_value[i-1], he_points[i-1])
                await ctx.send(f"Incorrect, question is now of {ceil(he_value[i-1])} points")
        else:
            await ctx.send("Invalid Answer")

    await ctx.send("Hurry-Up EM Complete")
    await outChannel.send("Hurry-Up EM Complete")


@bot.command(name="hx", help="Start Hurry-Up Extra round")
@commands.has_role('mock')
async def hx(ctx):

    global points_scored
    hx_value = deepcopy(hx_points)

    channel = ctx.message.channel

    if out_channel[ctx.message.guild.id] == -1:
        await ctx.send("Please set Output Channel")
        return False

    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = hx_ans[i-1]
        return ((abs(ans-cor)/cor)<(pres_range/2))

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>0:
            return cur
        else:
            return 0

    await ctx.send("Asking Questions..... \nHurry-Up Other")

    i = 1
    while i<=len(hx_ans):
        qn = "pb2019/images/x" + str(i) + ".PNG"
        await ctx.send(file=discord.File(qn))
        await ctx.send(f"{ceil(hx_value[i-1])} points")        
       
        msg = await bot.wait_for('message', check=check)

        if msg.content.lower() == "skip":
            await ctx.send("Skipped")
            points_scored[ctx.message.guild.id] -= 1
            await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
            i += 1
        elif msg.content.lower() == "exit":
            await ctx.send("Stopped")
            break
        elif msg.content.replace('.', '', 1).isdigit():
            r = float(msg.content)
            await ctx.send(f"Recorded answer is {r}")
            await outChannel.send(f"Hurry X {i} = {r}")
            if validate(r, i):
                points_scored[ctx.message.guild.id] += ceil(hx_value[i-1])
                await ctx.send(f"Correct, {ceil(hx_value[i-1])} points awarded")
                await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")
                i += 1
            else:
                hx_value[i-1] = reduce(hx_value[i-1], hx_points[i-1])
                await ctx.send(f"Incorrect, question is now of {ceil(hx_value[i-1])} points")
        else:
            await ctx.send("Invalid Answer")

    await ctx.send("Hurry-Up Other Complete")
    await outChannel.send("Hurry-Up Other Complete")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.channel.DMChannel):
        await message.channel.send("I don't talk in DMs.")
        return

    await bot.process_commands(message)


bot.run(TOKEN)

