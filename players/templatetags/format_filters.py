from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def format_wikipedia_url(parameter):
    return "https://ja.wikipedia.org/wiki/" + parameter if parameter else ''

@register.filter
def format_youtube_url(parameter):
    return "https://www.youtube.com/watch?v=" + parameter if parameter else ''

# 16進カラーコードをRGB形式に変換
@register.filter
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))

@register.filter
def format_decimal_trim(value):
    try:
        d = Decimal(value)
        # 小数点がある場合だけ処理する
        if d == d.to_integral():
            return str(d.quantize(Decimal('1')))
        else:
            return str(d.normalize())
    except (InvalidOperation, TypeError, ValueError):
        return '0'

@register.filter
def hit_mark(is_hit):
    if is_hit is True:
        return "○"
    elif is_hit is False:
        return "×"
    return ""  # Noneやnullのときは空文字

@register.filter
def join_mark(draft):
    if draft.is_joined is True:
        return "入団"
    elif draft.is_hit is False:
        return ""
    else:
        return "入団拒否"

@register.filter
def format_year(value):
    try:
        value = int(value)
        if value == 9000:
            value = "NPB"
        elif value == 9001:
            value = "MLB"
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
def format_batting_stats(plate_appearances, batting_average, home_runs, runs_batted_in, stolen_bases):
    if plate_appearances and plate_appearances != 0:
        avg_str = format_batting_average(batting_average)
        hr = format_integer(home_runs)
        rbi = format_integer(runs_batted_in)
        sb = format_integer(stolen_bases)
        return f"{avg_str} {hr}本 {rbi}点 {sb}盗塁"
    else:
        return "出場無し"

@register.simple_tag
def format_pitching_stats(games, earned_run_average, wins, loses, saves, holds, strike_outs):
    if games and games != 0:
        earned_average_str = format_pitching_average(earned_run_average)
        win = format_integer(wins)
        lose = format_integer(loses)
        save = format_integer(saves)
        hold = format_integer(holds)
        strike_out = format_integer(strike_outs)
        return f"{earned_average_str} {win}勝 {lose}敗 {save}S {hold}H {strike_out}奪"
    else:
        return "登板無し"

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
