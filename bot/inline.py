from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def app_start():
    inline_kb_list = [
        [
            InlineKeyboardButton(text="📋 Расчитать карту",
                              callback_data='chart'),
            InlineKeyboardButton(text="ℹ️ Узнать обо мне побольше",
                              callback_data='about')
        ],
        [
            InlineKeyboardButton(text="🐙 My_Git",
                            url='https://github.com/EgorkaPimp/SmartBudge_bot'),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)