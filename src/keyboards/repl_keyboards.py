from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from django.template.defaultfilters import first

from src.settings import APP_SETTINGS
from src.database.dao import PaySettingsDAO


def create_start_keyboard_inline():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text=f"Контент за {APP_SETTINGS.PRICE1} рублей",
            callback_data=f"g_2000"
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text=f"Контент за {APP_SETTINGS.PRICE2} рублей",
            callback_data=f"g_5000"
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Помощь",
            callback_data=f"g_help"
        )
    )

    return keyboard.as_markup()


def create_start_keyboard_down():
    first_pay = PaySettingsDAO.find_one_or_none(user_friendly_id=1)
    second_pay = PaySettingsDAO.find_one_or_none(user_friendly_id=2)
    m = ReplyKeyboardBuilder()
    m.row(
        KeyboardButton(text=first_pay.btn_text),
        KeyboardButton(text=second_pay.btn_text),
    )
    m.row(
        KeyboardButton(text="Помощь"),
    )
    return m.as_markup(resize_keyboard=True)
