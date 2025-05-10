from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter(name="age_with_suffix")
def age_with_suffix(value):
    try:
        return f"{value}歳"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="year_with_suffix")
def year_with_suffix(value):
    try:
        return f"{value}年"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="rank_with_suffix")
def rank_with_suffix(value):
    try:
        return f"{value}位"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="height_with_suffix")
def height_with_suffix(value):
    try:
        height = format_decimal_trim(value)
        return f"{height}cm"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="weight_with_suffix")
def weight_with_suffix(value):
    try:
        weight = format_decimal_trim(value)
        return f"{weight}kg"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="with_brackets")
def with_brackets(value):
    try:
        return f"「{value}」"
    except ValueError:
        return value


@register.filter(name="homerun_with_suffix")
def homerun_with_suffix(value):
    try:
        homerun = format_integer(value)
        return f"{homerun}本"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="rbi_with_suffix")
def rbi_with_suffix(value):
    try:
        rbi = format_integer(value)
        return f"{rbi}点"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="steel_with_suffix")
def steel_with_suffix(value):
    try:
        steel = format_integer(value)
        return f"{steel}盗"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="hit_with_suffix")
def hit_with_suffix(value):
    try:
        hit = format_integer(value)
        return f"{hit}安打"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="win_with_suffix")
def win_with_suffix(value):
    try:
        win = format_integer(value)
        return f"{win}勝"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="lose_with_suffix")
def lose_with_suffix(value):
    try:
        lose = format_integer(value)
        return f"{lose}敗"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="save_with_suffix")
def save_with_suffix(value):
    try:
        save = format_integer(value)
        return f"{save}S"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="hold_with_suffix")
def hold_with_suffix(value):
    try:
        hold = format_integer(value)
        return f"{hold}H"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter(name="strike_with_suffix")
def strike_with_suffix(value):
    try:
        strike_out = format_integer(value)
        return f"{strike_out}奪"
    except (ValueError, TypeError):
        return value  # 数値以外の場合そのまま返す


@register.filter
def format_wikipedia_url(parameter):
    return "https://ja.wikipedia.org/wiki/" + parameter if parameter else ""


@register.filter
def format_youtube_url(parameter):
    return "https://www.youtube.com/watch?v=" + parameter if parameter else ""


# 16進カラーコードをRGB形式に変換
@register.filter
def hex_to_rgb(hex_color):
    if not hex_color:
        return "rgb(255, 255, 255)"  # デフォルト値や空白を返してもOK
    hex_color = hex_color.lstrip("#")
    return ", ".join(str(int(hex_color[i : i + 2], 16)) for i in (0, 2, 4))


@register.filter
def format_decimal_trim(value):
    try:
        d = Decimal(value)
        # 小数点がある場合だけ処理する
        if d == d.to_integral():
            return str(d.quantize(Decimal("1")))
        else:
            return str(d.normalize())
    except (InvalidOperation, TypeError, ValueError):
        return "0"


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
def format_year(value, mlb_exists=True):
    try:
        value = int(value)
        if value == 9000:
            value = "NPB通算" if mlb_exists else "通算"
        elif value == 9001:
            value = "MLB通算" if mlb_exists else "通算"
        else:
            value = f"{value}年"
    except (TypeError, ValueError, InvalidOperation):
        return "0"

    return value


@register.filter
def format_batting_average(value):
    try:
        value = Decimal(value)
    except (TypeError, ValueError, InvalidOperation):
        return ".000"

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
        return "0.00"

    return f"{value:.2f}"


@register.filter
def format_integer(value):
    try:
        value = int(value)
    except (TypeError, ValueError, InvalidOperation):
        return "0"

    return value


@register.simple_tag
def format_batting_stats(
    plate_appearances, batting_average, home_runs, runs_batted_in, stolen_bases
):
    if plate_appearances and plate_appearances != 0:
        avg_str = format_batting_average(batting_average)
        hr = homerun_with_suffix(home_runs)
        rbi = rbi_with_suffix(runs_batted_in)
        sb = steel_with_suffix(stolen_bases)
        return f"{avg_str} {hr} {rbi} {sb}"
    else:
        return "出場無し"


@register.simple_tag
def format_pitching_stats(
    games, earned_run_average, wins, loses, saves, holds, strike_outs
):
    if games and games != 0:
        earned_average_str = format_pitching_average(earned_run_average)
        win = win_with_suffix(wins)
        lose = lose_with_suffix(loses)
        save = save_with_suffix(saves)
        hold = hold_with_suffix(holds)
        strike_out = strike_with_suffix(strike_outs)
        return f"{earned_average_str} {win} {lose} {save} {hold} {strike_out}"
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


@register.filter
def get_dynamic_field(record, field_name):
    """フィールド名を動的に受け取って値を取り出す（モデルにも辞書にも対応）"""
    if not record or not field_name:
        return None
    if isinstance(record, dict):
        return record.get(field_name)
    return getattr(record, field_name, None)


@register.filter
def get_position_short_name(position_name):
    return position_name[0]


@register.filter
def dict_get(d, key):
    return d.get(key)


@register.filter
def get_miss_text(value):
    miss_text = ""
    for i in range(value):
        miss_text += "外れ"

    return miss_text
