import pickle

birthdays = { }

class BDay:
    def __init__(self, month, day):
        self.month = month
        self.day = day
        return


def add_user(user_id, month, day):
    birthdays[user_id] = BDay(month, day)
    write_to_pickle()


def get_user(user_id):
    return birthdays[user_id]


def remove_user(user_id):
    del birthdays[user_id]
    write_to_pickle()


def read_from_pickle():
    try:
        with open("birthday_list", "rb") as file:
            global birthdays
            birthdays = pickle.load(file)
    except Exception as e:
        print("Exception in populate_users: " + str(e))


def write_to_pickle():
    with open("birthday_list", "wb") as file:
        pickle.dump(birthdays, file)


def get_todays_birthdays(month, day):
    birthday_users = []
    for key in birthdays.keys():
        if birthdays[key].month == month and birthdays[key].day == day:
            birthday_users.append(key)
    return birthday_users
