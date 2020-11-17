import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from math import ceil

major_ans = [0.17,36,0.99,836,3010000,65,777,66.7,52.9,
            7.8,0.0344,31.3,0.00005,8.17173,5.54,0.14,3600,18800,1.7,
            22600,22.63,0.025,0.19,0.976,0.768,1.88,143,1.96,0.09375,
            1300000,0.0000629,6.41874,24.4,0.303,3.6,0.16506,0.3292,2,0.009,7.81,
            0,1.26,200,512,0.333,31.3,0.000001,3.3,11.15,28700]
major_points = [3,3,3,3,3,4,4,4,4,4,3,4,4,4,5,4,4,4,4,6,4,4,5,6,3,4,5,5,5,5,5,5,6,5,4,6,6,4,6,6,7,6,6,5,6,5,7,6,8,9]
major_value = [3,3,3,3,3,4,4,4,4,4,3,4,4,4,5,4,4,4,4,6,4,4,5,6,3,4,5,5,5,5,5,5,6,5,4,6,6,4,6,6,7,6,6,5,6,5,7,6,8,9]

hm_ans = [40, 7040000, 150.6, 28]
hm_points = [3, 3, 4, 4]
hm_value = [3, 3, 4, 4]

he_ans = [2670, 0.4762, 1.62, 0.11]
he_points = [3, 3, 4, 4]
he_value = [3, 3, 4, 4]

hx_ans = [80, 20000000000, 5240000000000, 99]
hx_points = [3]*4
hx_value = [3]*4

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
        print(guild.id)
        points_scored[guild.id] = 0
        out_channel[guild.id] = None

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.command(name="test")
async def test(ctx):
    print(ctx.message.guild.id)
    print(points_scored)
    print(out_channel)
    await ctx.send("yeet")
    qn = "x1.png"
    await ctx.send(file=discord.File(qn))

@bot.command(name="out")
@commands.has_role('mock')
async def out(ctx, num:int):
    global out_channel
    out_channel[ctx.message.guild.id] = num
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])
    await ctx.send(f"Output set to {out_channel[ctx.message.guild.id]}")
    await outChannel.send(f"Output set to {out_channel[ctx.message.guild.id]}")


@bot.command(name="add")
@commands.has_role('mock')
async def add(ctx, num:int):
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])
    global points_scored
    points_scored[ctx.message.guild.id] += num
    await ctx.send(f"{num} points added")
    await outChannel.send(f"Total points {points_scored[ctx.message.guild.id]}")



@bot.command(name="major")
@commands.has_role('mock')
async def major(ctx):

    global points_scored, major_value

    channel = ctx.message.channel
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = major_ans[i-1]
        return ((abs(ans-cor)/cor)<0.05)

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>1:
            return cur
        else:
            return 1

    await ctx.send("Asking Questions.....\nMajor")

    i = 1
    while i<=50:

        qn = "pb/" + str(i) + ".png"
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

@bot.command(name="hm")
@commands.has_role('mock')
async def hm(ctx):

    global points_scored, hm_value

    channel = ctx.message.channel
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = hm_ans[i-1]
        return ((abs(ans-cor)/cor)<0.025)

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>0:
            return cur
        else:
            return 0

    await ctx.send("Asking Questions..... \nHurry-Up Mechanics")

    i = 1
    while i<=4:
        qn = "pb/m" + str(i) + ".png"
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

@bot.command(name="he")
@commands.has_role('mock')
async def he(ctx):

    global points_scored, he_value

    channel = ctx.message.channel
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = he_ans[i-1]
        return ((abs(ans-cor)/cor)<0.025)

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>0:
            return cur
        else:
            return 0

    await ctx.send("Asking Questions..... \nHurry-Up EM")

    i = 1
    while i<=4:
        qn = "pb/e" + str(i) + ".png"
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

@bot.command(name="hx")
@commands.has_role('mock')
async def hx(ctx):

    global points_scored, hx_value

    channel = ctx.message.channel
    outChannel = bot.get_channel(out_channel[ctx.message.guild.id])

    def check(m):
        return m.channel == channel

    def validate(ans, i):
        cor = hx_ans[i-1]
        return ((abs(ans-cor)/cor)<0.025)

    def reduce(cur, orignal):
        cur -= 0.2*orignal
        if cur>0:
            return cur
        else:
            return 0

    await ctx.send("Asking Questions..... \nHurry-Up Other")

    i = 1
    while i<=4:
        qn = "pb/x" + str(i) + ".png"
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

