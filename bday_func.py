import bday_date as date
import birthday_pickle as pickle
import re

date_error_string = "\nDate was incorrectly entered. Please enter the date as...\n" \
                    "```MM-DD (03/04, 3/4, 03/4, 3/04)\n" \
                    "MM/DD (03-04, 3-4, 03-4, 3-04)\n" \
                    "MM DD (03 04, 3 4, 03 4, 3 04)\n" \
                    "[Full Month Name] DD (September 21, April 03, January 9)```"


def get_todays_birthdays(month, day):
    return pickle.get_todays_birthdays(month, day)


def get_birthday_error():
    return "You need a command!"


def populate_birthdays():
    pickle.read_from_pickle()


def get_birthday(author, args, mentions, client):
    """
    Finds the birthday associated with the mem_request
    :param author: Member - message author
    :param args:
    :param mentions:
    :param client:
    :return: a string response that the bot will say to the request
    """

    try:
        mem_request = args[1]
    except:
        return "No member was inputted. :x: Type get {me | [@user mention]}"

    if mem_request == "me":
        print("Requesting their own birthday")
        if author.id in pickle.birthdays:
            curr_birthday = pickle.get_user(author.id)
            return "Your birthday is on {0} {1}".format(date.to_month_name(curr_birthday.month), curr_birthday.day)
        else:
            return "Your birthday has not been set!"
    elif len(mentions) is not 0:
        for mention in mentions:
            if mention.id == client.user.id:
                return "I don't have a birthday. :robot: However, if you want to know when I was created, it was at 4/5/2018 at approximately 4:13pm! :desktop:"
            if mention.id in pickle.birthdays:
                curr_birthday = pickle.birthdays[mention.id]
                if mention.id == author.id:
                    return "Your birthday is on {0} {1}".format(date.to_month_name(curr_birthday.month), str(curr_birthday.day))
                return "{0}'s birthday is on {1} {2}".format(mention.name, date.to_month_name(curr_birthday.month), str(curr_birthday.day))
            else:
                return "{0}'s birthday has not been set up yet!".format(mention.name)

    return "Member couldn't be detected. Find a member's birthday by typing get {me | [@user mention]}"


def set_birthday(author, args):
    """
    Sets the birthday of the message author if the message author has not set their birthday. Otherwise
    :param author: Member - message author
    :param args: arguments
    :return: a string response that the bot will say to the request
    """

    try:
        date_pattern = re.compile("[0-9]?[0-9][-\/][0-9]?[0-9]")
        if date_pattern.fullmatch(args[1]) is not None:
            arg_split = re.split("[-\/]", args[1])
            month = arg_split[0]
            day = arg_split[1]
            print("Regex calculated month: {0} day: {1}".format(month, day))
        else:
            month = args[1]
            day = int(args[2])
            print("Calculated month: {0} day: {1}".format(month, day))
    except:
        print("Date format incorrect")
        return date_error_string

    if not date.is_valid_date(month, day):
        print("Date format correct - Date outside calendar range")
        return "The date you entered was either invalid or incorrectly formatted. :x:"

    conv_month = date.to_month_index(month)
    conv_day = int(day)

    pickle.add_user(str(author.id), conv_month, conv_day)

    success = pickle.birthdays[str(author.id)]
    print("Date set successful")
    return "Your birthday was successfully set to {0} {1} :ok_hand:".format(date.to_month_name(success.month), success.day)


def del_birthday(author, admin_list, mentions):
    if author.id in admin_list:
        if mentions[0].id in pickle.birthdays:
            pickle.remove_user(mentions[0].id)
            print("Birthday removal successful")
            return "{0}'s birthday was successfully removed. :ok_hand:".format(mentions[0].name)
        else:
            print("User birthday not pickled")
            return "I'm sorry, I don't know {0}'s birthday, so I can't forget it. :robot:".format(mentions[0].name)
    else:
        print("User does not have access to command")
        return ":x: You don't have access to that command! :x:"
