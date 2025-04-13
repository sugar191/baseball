from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def format_year(value):
    try:
        value = int(value)
        if value == 9000:
            value = "国内通算"
        elif value == 9001:
            value = "海外通算"
    except (TypeError, ValueError, InvalidOperation):
        return '0'
    
    return value

@register.filter
def format_batting_average(value):
    try:
        value = Decimal(value)
    except (TypeError, ValueError, InvalidOperation):
        return '.000'

    formatted = f"{value:.3f}"
    if value < 1:
        return formatted[1:]  # 先頭の「0」を消す → ".000"
    else:
        return formatted  # 例: "1.000"

@register.filter
def format_pitching_average(value):
    try:
        value = Decimal(value)
    except (TypeError, ValueError, InvalidOperation):
        return '0.00'
    
    return f"{value:.2f}"

@register.filter
def format_integer(value):
    try:
        value = int(value)
    except (TypeError, ValueError, InvalidOperation):
        return '0'
    
    return value

@register.simple_tag
def format_batting_stats(average, homeruns, rbi, steals):
    # 各値のフォーマット
    avg_str = format_batting_average(average)
    hr = format_integer(homeruns)
    rbi = format_integer(rbi)
    sb = format_integer(steals)

    return f"{avg_str} {hr}本 {rbi}点 {sb}盗塁"

@register.simple_tag
def format_pitching_stats(earned_average, win, lose, save, hold, strike_out):
    # 各値のフォーマット
    earned_average_str = format_pitching_average(earned_average)
    win = format_integer(win)
    lose = format_integer(lose)
    save = format_integer(save)
    hold = format_integer(hold)
    strike_out = format_integer(strike_out)

    return f"{earned_average_str} {win}勝{lose}敗{save}S{hold}H {strike_out}奪"

@register.filter
def format_salary(salary):
    try:
        salary = float(salary)
    except (TypeError, ValueError):
        return ""

    if salary == int(salary):
        formatted_num = int(salary)
    else:
        formatted_num = salary

    units = [("億", 10**8), ("万", 10**4), ("", 1)]
    result = []

    for unit, value in units:
        if formatted_num >= value:
            result.append(f"{int(formatted_num // value)}{unit}")
            formatted_num %= value

    return "".join(result)
