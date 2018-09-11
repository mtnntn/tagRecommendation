
def percentage(num, total, precision=1, to_str=False, par=True):
    percent = num / total * 100
    rounded = round(percent, precision)
    if to_str:
        rounded_str = str(rounded) + "%"
        if par:
            return "(" + rounded_str + ")"
        return rounded_str
    return rounded
