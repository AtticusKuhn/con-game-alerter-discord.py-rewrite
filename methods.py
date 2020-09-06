from data.config import CONFIG

def seconds_to_time(seconds:int):
    print(seconds)
    seconds = seconds % (24 * 3600) 
    day = seconds // 86400
    seconds %= 86400
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    day =int(day)
    hour = int(hour)
    minutes= int(minutes)
    seconds = int(seconds)
    day = ("1 day " if day==1 else "") if day==0 else f'{day} days '
    hour = ("1 hour " if hour==1 else "") if hour==0 else f'{hour} hours '
    minutes = ("1 minute " if minutes==1 else "") if minutes==0 else  f'{minutes} minutes '
    seconds = ("1 second" if seconds==1 else "" )if seconds==0 else  f'{seconds} seconds'
    return day+hour+minutes+seconds 


def parse_costs(cost_string):
    cost_string = cost_string.replace("=",":")
    cost_string = cost_string.replace(",",",\n")
    cost_string = cost_string.replace("a20","manpower")
    cost_string = cost_string.replace("a1","supplies")
    cost_string = cost_string.replace("a2","components")
    cost_string = cost_string.replace("a3","money")
    cost_string = cost_string.replace("a4","rares")
    cost_string = cost_string.replace("a5","fuel")
    cost_string = cost_string.replace("a6","electronics")
    return cost_string


def parse_format(possible_format):
    possible_format=str(possible_format)
    possible_format=possible_format.strip()
    if possible_format=="all":
        return "all"
    for format, aliases  in CONFIG.formats.items():
        if format.lower()==possible_format.lower():
            return format
        if possible_format.lower() in aliases:
            return format
    return False
