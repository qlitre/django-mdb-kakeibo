from .seaborn_colorpalette import sns_paired
from typing import Literal


def add_prev_and_next_month_year_to_context(context, year, month):
    """前月、前年、次月、次年をcontextに与えて返す"""

    if month == 12:
        prev_month = 11
        prev_year = year
        next_month = 1
        next_year = year + 1
    elif month == 1:
        prev_month = 12
        prev_year = year - 1
        next_month = 2
        next_year = year
    else:
        prev_month = month - 1
        prev_year = year
        next_month = month + 1
        next_year = year

    context['prev_year'] = prev_year
    context['prev_month'] = prev_month
    context['next_year'] = next_year
    context['next_month'] = next_month

    return context


def add_colormap_to_context(context, queryset, graph_labels):
    """グラフのラベルに対応したcolor mapをcontextに与えて返す"""
    color_map = sns_paired()
    color_dict = {}
    for i, c in enumerate(queryset):
        color_dict[c.name] = color_map[i]

    context['color_map'] = [color_dict.get(c) for c in graph_labels]

    return context


def success_message_for_item(register_or_delete_string: Literal['Register', 'Delete'],
                             target_model_name: Literal['Payment', 'Income', 'Asset'],
                             date, category, amount):
    """サクセスメッセージを作って返す"""

    msg = f"""
    Successfully {register_or_delete_string} {target_model_name}\n
    Date:{date}\n
    Category:{category}\n
    Amount:{amount}
    """
    return msg

