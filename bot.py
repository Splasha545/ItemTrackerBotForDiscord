import random
import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix='.')
items = {}
db = sqlite3.connect('flatItems.db')


def create_table():
    cur = db.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS items
                   (name text PRIMARY KEY,
                    quantity real
                    )'''
                )
    # Save (commit) the changes
    db.commit()


def generateListEmbed():
    em = discord.Embed(
        title=" ⚒ Items ⚒️",
        colour=discord.Colour.blue()
    )
    field = ""
    cur = db.cursor()
    for row in cur.execute("SELECT * FROM items"):
        # if (len(field > 1000)):
        #    field2
        field += f":white_small_square: {row[0]} : {row[1]}\n"
    em.add_field(name="\u200b", value=field, inline=True)
    print(len(field))
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
    print("help")
    create_table()
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


@bot.command(aliases=['newitem', 'new'])
async def newItem(ctx, *, key):
    cur = db.cursor()
    all_keys_list = []
    all_keys = cur.execute('SELECT name FROM items').fetchall()
    for tuple in all_keys:
        all_keys_list.append(tuple[0])
    if key not in all_keys_list:
        cur.execute("INSERT INTO items VALUES (?, ?)", (key, 0))
        db.commit()
        em = generateNewEmbed(key)
        await ctx.send(embed=em)
    else:
        await ctx.send("This item is already present on the list!")


@bot.command(aliases=['removeitem', 'remove'])
async def removeItem(ctx, key):
    cur = db.cursor()
    all_keys_list = []
    all_keys = cur.execute('SELECT name FROM items').fetchall()
    for tuple in all_keys:
        all_keys_list.append(tuple[0])
    if key not in all_keys_list:
        await ctx.send("No such item is in the list.")
    else:
        cur.execute("DELETE FROM items WHERE name = ?", [key])
        db.commit()
        em = generateRemoveEmbed(key)
        await ctx.send(embed=em)


@bot.command(aliases=['quantity', 'edit'])
async def editItemQuantity(ctx, key, addValue):
    cur = db.cursor()
    quantity_at_key = cur.execute("SELECT quantity FROM items WHERE name = ?", [key]).fetchone()[0]
    if float(quantity_at_key) + float(addValue) < 0:
        await ctx.send(
            f"That's impossible. You have {quantity_at_key} of {key} and {quantity_at_key} + {addValue} is less than 0")
    else:
        cur.execute("UPDATE items SET quantity = ? WHERE name = ?", (float(quantity_at_key) + float(addValue), key))
        db.commit()
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command(aliases=['set'])
async def setQuantity(ctx, key, arg):
    if int(arg) < 0:
        await ctx.send(f"What is wrong with you? {arg} is a negative number :/")
    else:
        cur = db.cursor()
        cur.execute("UPDATE items SET quantity = ? WHERE name = ?", (float(arg), key))
        db.commit()
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command(aliases=['+item', 'additem', '+1'])
async def add1Item(ctx, key):
    cur = db.cursor()
    previous_quantity = cur.execute("SELECT quantity FROM items WHERE name = ?", [key]).fetchone()[0]
    print(previous_quantity)
    cur.execute("UPDATE items SET quantity = ? WHERE name = ?", (float(previous_quantity) + 1, key))
    db.commit()
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command(aliases=['-item', '-1'])
async def subtractItem(ctx, key):
    cur = db.cursor()
    previous_quantity = cur.execute("SELECT quantity FROM items WHERE name = ?", [key]).fetchone()[0]
    if float(previous_quantity) == 0:
        await ctx.send("You cant have less than 0 of some item :/")
    else:
        cur.execute("UPDATE items SET quantity = ? WHERE name = ?", (float(previous_quantity) - 1, key))
        db.commit()
    em = generateListEmbed()
    await ctx.send(embed=em)


@bot.command(aliases=['show'])
async def displayEmbed(ctx):
    em = generateListEmbed()
    await ctx.send(embed=em)
    cur = db.cursor()
    list = []
    list = cur.execute("SELECT name FROM items WHERE quantity = 0").fetchall()
    if len(list) > 0:
        reply = "We have run out of: "
        for i in range(0, len(list)):
            if i < len(list) - 1:
                reply += f"{list[i]}, "
            else:
                reply += f"{list[i]}."
        await ctx.send(reply)


@bot.command()
async def _help_(ctx):
    em = discord.Embed(
        colour=discord.Colour.dark_gold(),
        title="Commands:"
    )
    em.add_field(name="__newItem__ \n(alternatively __new__)", value="example: **.newItem <item name>**"
                                           "\nThis command adds a new item to the list.", inline=False)
    em.add_field(name="__removeItem__ \n(alternatively __remove__", value="example: **.removeItem <item name>**"
                                              "\nThis command removes some item from the list.", inline=False)
    em.add_field(name="__editItemQuantity__ \n(alternatively __edit__ or __quantity__)",
                 value="example: **.edit <item name> <number>** "
                       "\nThis command changes the quantity of some "
                       "item by the number given (it can be positive or negative)", inline=False)
    em.add_field(name="__setQuantity__ \n(alternatively __set__)",
                 value="example: **.set <item name> <number>**"
                       "\nThis command sets the quantity of the given item", inline=False)
    em.add_field(name="__add1Item__ \n(alternatively __+item__ or __+1__)",
                 value="example: **.+item <item name>**"
                       "\nThis command increases the quantity of given item by 1", inline=False)
    em.add_field(name="__subtractItem__ \n(alternatively __-item__ or __-1__)",
                 value="example: **.-item <item name>**"
                       "\nThis command decreases the quantity of given item by 1", inline=False)
    em.add_field(name="__show__",
                 value="example: **.show** \nThis command displays all the information on each item we have.")
    em.set_footer(text="❗❗ *Remember to always add a '.' before any command ❗❗")
    await ctx.send(embed=em)


# @bot.event
# async def on_message(message):
#    await message.reply(":white_small_square:")

bot.run("token")
