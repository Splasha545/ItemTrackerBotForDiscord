import random

import discord
from discord import *
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
items = {}


def generateListEmbed():
    em = discord.Embed(
        title=" ⚒ Items ⚒️",
        colour=discord.Colour.blue()
    )
    field = ""
    for key in items.keys():
        field += f":white_small_square: {key} : {items[key]}\n"
    em.add_field(name=field, value="\u200b", inline=True)
    return em


def generateNewEmbed(key):
    em = discord.Embed(
        title="✅ Item added ✅",
        colour=discord.Colour.green()
    )
    em.add_field(name="\u200b", value=f"***{key}*** was added to the list 👍")
    return em


def generateRemoveEmbed(key):
    em = discord.Embed(
        title="❌ Item removed ❌",
        colour=discord.Colour.red()
    )
    em.add_field(name="\u200b", value=f"***{key}*** was removed from the list 👍")
    return em


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("with your private information"))
    print("Bot online!")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! \n {round(bot.latency * 1000)}ms")


@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, args):
    responses = ["It is certain",
                 "It is decidedly so",
                 "Without a doubt",
                 "Yes, definitely",
                 "You may rely on it",
                 "As I see it, yes",
                 "Most likely",
                 "Outlook good",
                 "Yes",
                 "Signs point to yes",
                 "Reply hazy try again",
                 "Ask again later",
                 "Better not tell you now",
                 "Cannot predict now",
                 "Concentrate and ask again",
                 "Don't count on it",
                 "My reply is no",
                 "My sources say no",
                 "Outlook not so good",
                 "Very doubtful"]
    await ctx.send(random.choice(responses))


@bot.command()
async def newItem(ctx, *, key):
    if key not in items:
        items.update({key: 0})
        print(items)
        em = generateNewEmbed(key)
        await ctx.send(embed=em)


@bot.command(aliases=['removeitem'])
async def removeItem(ctx, *, key):
    if key not in items:
        ctx.send("No such item is in the list.")
    else:
        items.pop(key)
        print(items)
        em = generateRemoveEmbed(key)
        await ctx.send(embed=em)


@bot.command(aliases=['quantity', 'edit'])
async def editItemQuantity(ctx, key, addValue):
    if items[key] + int(addValue) < 0:
        await ctx.send(f"Thats impossible. You have {items[key]} of {key} and {items[key]} + {addValue} is less than 0")
    else:
        items[key] += int(addValue)
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command(aliases=['set'])
async def setQuantity(ctx, key, arg):
    if int(arg) < 0:
        await ctx.send(f"What is wrong with you? {arg} is a negative number :/")
    else:
        items[key] = int(arg)
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command(aliases=['+item', 'additem', '+1'])
async def add1Item(ctx, *, key):
    items[key] += 1
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command(aliases=['show'])
async def displayEmbed(ctx):
    em = generateListEmbed()
    await ctx.send(embed=em)
    list = []
    for key in items.keys():
        if items[key] == 0:
            list.append(key)
    if len(list) > 0:
        reply = "We have run out of: "
        for i in range(0, len(list)):
            if i < len(list) - 1:
                reply += f"{list[i]}, "
            else:
                reply += f"{list[i]}."
        await ctx.send(reply)


@bot.command(aliases=['-item', '-1'])
async def subtractItem(ctx, *, key):
    if items[key] == 0:
        await ctx.send("You cant have less than 0 of some item :/")
    else:
        items[key] -= 1
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command()
async def _help_(ctx):
    em = discord.Embed(
        colour=discord.Colour.dark_gold(),
        title="Commands:"
    )
    em.add_field(name="__newItem__", value="example: **.newItem <item name>**"
                                           "\nThis command adds a new item to the list.", inline=False)
    em.add_field(name="__removeItem__", value="example: **.removeItem <item name>**"
                                              "\nThis command removes some item from the list.", inline=False)
    em.add_field(name="__editItemQuantity__ \n(alternatively __edit__ or __quantity__)",
                 value="example: **.edit <item name> <number>** "
                       "\nThis command changes the quantity of some "
                       "item by the number given (it can be positive or negative)", inline=False)
    em.add_field(name="__setQuantity__ \n(alternatively __set__)",
                 value="example: **.set <item name> <number>**"
                       "\nThis command sets the quantity of the given item", inline=False)
    em.add_field(name="__add1Item__ \n(alternatively __+item__)",
                 value="example: **.+item <item name>**"
                       "\nThis command increases the quantity of given item by 1", inline=False)
    em.add_field(name="__subtractItem+_ \n(alternatively __-item__",
                 value="example: **.-item <item name>**"
                       "\nThis command decreases the quantity of given item by 1", inline=False)
    em.add_field(name="__show__",
                 value="example: **.show** \nThis command displays all the information on each item we have.")
    em.set_footer(text="❗❗ *Remember to always add a '.' before any command ❗❗")
    await ctx.send(embed=em)


# @bot.event
# async def on_message(message):
#    await message.reply(":white_small_square:")


bot.run("ODcyMDYxMTgxMjMyMjk1OTM2.YQkYQw.5b-uEApz0buBjUvonqdKQ1_dFgA")
