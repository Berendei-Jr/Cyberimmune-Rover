def colored_text(text, color):
    match color:
        case "red":
            return "\033[31m{}\033[0m".format(text)
        case "green":
            return "\033[32m{}\033[0m".format(text)
        case "yellow":
            return "\033[33m{}\033[0m".format(text)
        case _:
            return text


def pretty_list(list: list):
    return "".join(["\n => " + str(item) for item in list])
