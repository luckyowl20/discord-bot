import discord
from discord.ext import commands
import img_search as su
import random
from corona import analysis as ana

client = commands.Bot(command_prefix='.')

DRIVER_PATH = 'chromedriver.exe'


# client decorator after client name above
@client.event
async def on_ready():
    print('Bot is ready!')


@client.event
async def on_message(message):
    if message.content == "That's cool 😎":
        await message.add_reaction("😎")

    await client.process_commands(message)


# name the function what you want the command to be
@client.command()
async def ping(ctx):
    """Shows latency"""
    await ctx.send(f'Pong {round(client.latency * 1000)}ms')


@client.command()
async def fruit(ctx, query: str = "fruit", num_results: int = 1):
    """
    The command for when you want to search about fruit related images

    :param ctx: context, required by discord api
    :param query: what the user wants to search related to fruit
    :param num_results: how many results the user wants to display, max 5
    :return: your image (None)
    """
    print(f"\nfruit called: {query}, prev_searches: {su.prev_searches}")

    if num_results >= 6:
        num_results = 5
        await ctx.send("Please do not request more than 5 pieces of fruit at a time!")

    if query.lower() == "database":
        await ctx.send(f"Here are the current entries in the database: {su.prev_searches}")

    elif f"{query}_fruit.json" not in su.prev_searches:
        await ctx.send(f"You're the first person to search for '{query} fruit', please wait a moment")

    if query.lower() != "database":
        images, start, error = su.get_image(query.lower(), random.randint(0, 89), num_results, "fruit")

        if not error:
            for image in images:
                await ctx.send(f"**Here is some fruit:** {image} *(Search: '{query}', Image: {images.index(image) + 1}"
                               f" of {len(images)}, Starting Position: {start})*")
        else:
            await ctx.send(f"**Unable to search for your image, no more API requests** "
                           f"({su.get_key_info(su.api_keys_path)[1]}/{su.max_requests})")


@client.command()
async def google(ctx, start_number: int = 0, *args):
    """
    Googles the specified image, the number corresponds to which image is returned

    :param ctx: context, required by discord api
    :param start_number: which image you want
    :param args: your search
    :return: your image (None)
    """
    search = ""
    for arg in args:
        search += arg + " "
    search = search.rstrip(" ")

    if start_number > 93:
        await ctx.send(f"You cannot search past the 93rd image, this is the 93rd image")
        start_number = 93

    print(search)
    print(f"\nfruit called: {search}, {start_number} prev_searches: {su.prev_searches}")

    if search == "database":
        await ctx.send(f"Here are the current entries in the database: {su.prev_searches}")

    elif f"{search}_.json" not in su.prev_searches:
        await ctx.send(f"You're the first person to search for '{search}', please wait a moment")

    if search != "database":
        images, start, error = su.get_image(search, start_number)
        if not error:
            for image in images:
                await ctx.send(f"**Here is your image:** {image} *(Search: '{search}', Image: {images.index(image) + 1}"
                               f" of {len(images)}, Starting Position: {start})*")
        else:
            await ctx.send(f"**Unable to search for your image, no more API requests** "
                           f"({su.get_key_info(su.api_keys_path)[1]}/{su.max_requests})")


@client.command()
async def apinfo(ctx):
    """Gives information regarding the number of Google Images API requests to monitor usage"""
    key_info = su.get_key_info(su.api_keys_path)
    key_requests = ""
    for key in key_info[0]:
        key_requests += f"{key[0]}: {key[2]}, "
    key_requests = key_requests.rstrip(", ")
    await ctx.send(f"Total requests to API: {key_info[1]}/{su.max_requests} ({key_requests})")


@client.command()
async def corona(ctx):
    """
    A list of commands regarding coronavirus type .corona help for more information

    :param ctx: context, required by discord api
    :return: An image/text (None)
    """
    sub_command = ctx.message.content.lstrip(".corona ")
    ana.download_data()

    if sub_command.lower() == "help":
        await ctx.send(f"If you're looking to get information on the COVID-19 pandemic, heres some cool graphs "
                       f"type .corona (graph) to see a graph. Graph options are: world daily, us daily, world gr, "
                       f"us gr, top 10, total cases")

    elif sub_command.lower() == "world daily":
        await ctx.send("Here is the latest graph representing the number of cases reported around the world on a day "
                       "to day basis")
        await ctx.send(file=discord.File(ana.daily_cases_w()))

    elif sub_command.lower() == "us daily":
        await ctx.send("Here is the latest graph representing the number of cases reported around the US on a day "
                       "to day basis")
        await ctx.send(file=discord.File(ana.daily_cases_us()))

    elif sub_command.lower() == "world gr":
        await ctx.send("Here is the latest graph representing the growth rate of the infected population of the world")
        await ctx.send(file=discord.File(ana.world_growth_rate()))

    elif sub_command.lower() == "us gr":
        await ctx.send("Here is the latest graph representing the growth rate of the infected population of the US")
        await ctx.send(file=discord.File(ana.usa_growth_rate()))

    elif sub_command.lower() == "top 10":
        await ctx.send("Here are the top 10 countries by number of confirmed cases over time")
        await ctx.send(file=discord.File(ana.top10()))

    elif sub_command.lower() == "total cases":
        await ctx.send("Here is the latest graph representing the total number of confirmed cases in the world and in "
                       "the US")
        await ctx.send(file=discord.File(ana.confirmed_cases()))

    elif sub_command.lower() == "show all":
        await ctx.send("Here are all of the graphs:")
        await ctx.send(file=discord.File(ana.daily_cases_w()))
        await ctx.send(file=discord.File(ana.daily_cases_us()))
        await ctx.send(file=discord.File(ana.world_growth_rate()))
        await ctx.send(file=discord.File(ana.usa_growth_rate()))
        await ctx.send(file=discord.File(ana.top10()))
        await ctx.send(file=discord.File(ana.confirmed_cases()))

    else:
        await ctx.send("That command is not part of the corona command set, type '.corona help' for help")
        await ctx.send(f"'{sub_command}'")


@client.command()
async def pog(ctx):
    """Sends a PogU emote to the sender, special message for special users"""
    names = []
    for emoji in client.emojis:
        names.append(emoji.name)

    special_users = ["LuckyOwl"]

    if ctx.message.author.name in special_users:
        await ctx.send(f"{ctx.message.author.mention} {client.emojis[(names.index('PogU'))]} very cool")

    else:
        print(ctx.message.author.name)
        await ctx.send(f"{ctx.message.author.mention} {client.emojis[(names.index('PogU'))]}")


@client.command()
async def hate(ctx, user):
    """Send hatemail to someone, make sure to mention them with @(username)"""
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{user} I hate you")


@client.command()
async def fart(ctx):
    image, start, error = su.get_image("person farting", random.randint(0, 85), 1)
    await ctx.send(image[0])


@client.command()
async def cool(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("That's cool 😎")


@client.command()
async def delmsg(ctx, amount: int = 0):
    """Deletes a number of messages, for use by authorized users only"""
    # LuckyOwl, Supergoat, Jaws
    auth_users = [270372728614289409, 275454678853222401, 341787743690686465]

    if ctx.message.author.id in auth_users:
        await ctx.channel.purge(limit=amount + 1)


@client.command()
async def ustats(ctx):
    await ctx.send(f"{ctx.message.author, 1}")


client.run('NzA2OTcyNDExOTYyMzI3MTIw.XrVSmQ.SeoXspn-iZssuB3d3kCbEZHnEPo')
