import json
from datetime import datetime
from discord.ext.commands import Bot
import discord
import bday_func as birth_func
import asyncio

json_file = json.load(open("fk_bot-config.json", 'r'))


PREFIX = json_file['prefix']
TOKEN = json_file['token']
ADMINS = json_file['admins']
SERVER_ID = json_file['server_id']
CHANNEL_ID = json_file['channel_id']
CHANNEL = None
SERVER = None

client = Bot(command_prefix=PREFIX)


@client.command(name='birthday',
                description="Birthday functions allow the bot to give a user's birthday on demand and wish them a 'Happy Birthday' when it's their day.",
                brief="Get or set birthdays",
                pass_context=True)
async def birthday(context, *, Parameters=None):
    """
    Parameters:

        Set - Sets a birthday according to a given date
            usage: set [date]
                    [date] - Formatted as one of the following:
                            MM-DD (03/04, 3/4, 03/4, 3/04)
                            MM/DD (03-04, 3-4, 03-4, 3-04)
                            MM DD (03 04, 3 4, 03 4, 3 04)
                            [Full Month Name] DD (September 21, April 03, January 9)

        Get - Gets a birthday according to a given user
            usage: get [user]
                    [user] - One of the following:
                            @mention - gets the mentioned user's birthday
                            me - gets your birthday

        Delete - ADMIN CMD ONLY - Removes a birthday to a given user
            usage: delete [user]
                    [user] - One of the following:
                            @mention - removes the mentioned user's birthday
    """
    author = context.message.author
    channel = context.message.channel
    print("\n__________________")
    print("Birthday message from " + author.name)
    print("Message: " + context.message.content)
    print("Args: " + Parameters)
    try:
        msg = ""
        args = str(Parameters).split(" ")
        if args is None:
            msg = birth_func.get_birthday_error()
        elif args[0] == "get":
            print("Command type: get")
            msg = birth_func.get_birthday(author, args, context.message.mentions, client)
        elif args[0] == "set":
            print("Command type: set")
            msg = birth_func.set_birthday(author, args)
        elif args[0] == 'delete':
            print("Command type: delete")
            msg = birth_func.del_birthday(author, ADMINS, context.message.mentions)
        elif args[0] == "kill":
            msg = "Alright. Expect it soon."
        elif args[0] == "potato":
            msg = ":potato:"
        else:
            msg = "Command not recognized."
        print("__________________\n")
        await client.send_message(channel, "{0} {1}".format(author.mention, msg))
        return
    except Exception as e:
        print("Exception occurred while finding birthday info: " + str(e))

    print("__________________\n")

    await client.send_message(channel, "{0} There was an error processing your request. Please try again.".format(author.mention))


@client.event
async def on_ready():
    print("\n__________________")
    print("Logged in as:")
    print("Name: " + client.user.name)
    print("ID: " + client.user.id)
    print("__________________\n")
    birth_func.populate_birthdays()
    global CHANNEL
    CHANNEL = client.get_channel(CHANNEL_ID)
    global SERVER
    SERVER = client.get_server(SERVER_ID)


async def wait_for_new_day():
    await asyncio.sleep(86400)


async def check_for_new_day():
    await client.wait_until_ready()
    await noon_utc()
    while not client.is_closed:
        now_date = datetime.utcnow()
        birthday_users = birth_func.get_todays_birthdays(now_date.month, now_date.day)
        # server = client.get_server(SERVER_ID)
        if len(birthday_users) is not 0:
            birthday_str = "@everyone\n\n:birthday::cake::birthday::cake::birthday::cake::birthday::cake::birthday:" \
                           ":cake::birthday::cake::birthday::cake::birthday::cake::birthday::cake::birthday::cake:" \
                           ":birthday::cake::birthday::cake::birthday::cake::birthday::cake::birthday::cake:" \
                           ":birthday::cake::birthday::cake::birthday::cake:\n\n"
            for user in birthday_users:
                birthday_str += "{0} IT'S YOUR BIRTHDAY TODAY!!! :balloon::confetti_ball::balloon::confetti_ball:" \
                                ":balloon::confetti_ball::balloon::confetti_ball::balloon::confetti_ball::balloon:" \
                                ":confetti_ball::balloon::confetti_ball::balloon::confetti_ball::balloon:" \
                                ":confetti_ball::balloon::confetti_ball::balloon::confetti_ball::balloon:" \
                                "\n".format(SERVER.get_member(user).mention)
            birthday_str += "\n:birthday::cake::birthday::cake::birthday::cake::birthday::cake::birthday::cake:" \
                            ":birthday::cake::birthday::cake::birthday::cake::birthday::cake::birthday::cake:" \
                            ":birthday::cake::birthday::cake::birthday::cake::birthday::cake::birthday::cake:" \
                            ":birthday::cake::birthday::cake::birthday::cake:"
            await client.send_message(CHANNEL, birthday_str)
        await wait_for_new_day()


async def noon_utc():
    # match seconds
    print("AWAITING SECONDS SYNC")
    while True:
        now_time = datetime.utcnow()
        if now_time.second == 0:
            break
        else:
            await asyncio.sleep(1)
    print("AWAITING NOON SYNC {0}".format(datetime.utcnow()))
    #match time
    while True:
        now_date = datetime.utcnow()
        if now_date.hour == 0 and now_date.minute == 40:
            print("NOW NOON UTC: {0}".format(str(now_date)))
            return
        else:
            await asyncio.sleep(60)

print("Initializing")
client.loop.create_task(check_for_new_day())

client.run(TOKEN)


