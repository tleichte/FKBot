import calendar


def to_month_index(month):
    """Returns None if name doesn't exist, otherwise index in year"""
    try:
        int_month = int(month)
        if is_valid_month(month):
            return int_month
    finally:
        if month in calendar.month_name:
            return list(calendar.month_name).index(month)
    return None


def to_month_name(month):
    """Returns None if index is not int or is not within month names"""
    if is_valid_month(month):
        try:
            return calendar.month_name[int(month)]
        except:
            return month
    return None


def is_valid_month(month):
    """Returns true upon valid month input"""
    try:
        int_month = int(month)
        if 1 <= int_month <= 12:
            return True
    except ValueError:
        if str(month) in calendar.month_name:
            return True
    return False


def is_valid_day(month, day):
    """Returns true upon valid day input"""
    try:
        day_int = int(day)
        month_int = to_month_index(month)
        if (day_int < 1 or day_int > 31)\
            or (month_int == 2 and day_int > 29)\
                or ((month_int == 4 or month_int == 6 or month_int == 9 or month_int == 11) and day_int > 30):
            return False
        return True
    except:
        return False
    return False


def is_valid_date(month, day):
    valid_month = is_valid_month(month)
    valid_day = is_valid_day(month, day)
    print("Is valid month: {0}, Is valid day: {1}".format(valid_month, valid_day))
    return valid_month and valid_day
