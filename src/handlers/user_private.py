import io
from datetime import date, datetime

from aiogram import Router, F, Bot, types
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery, BufferedInputFile

from src.database.dao import ClientDao, BinaryDocumentDAO, HelloMessageDAO, PaySettingsDAO, HelpChatDAO
from src.database.models import Status
from src.filters.chat_types import ChatTypesFilter
from src.keyboards.repl_keyboards import create_start_keyboard_down

from src.settings import APP_SETTINGS

user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter(["private"]))


@user_private_router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    await start_message(chat_id=message.chat.id, bot=bot, username=message.from_user.username)


@user_private_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def start_message(chat_id, bot: Bot, username):
    client = ClientDao.find_one_or_none(id=chat_id)
    hello_message = HelloMessageDAO.find_one_or_none(user_friendly_id=1)
    if hello_message is None:
        text = APP_SETTINGS.HELLO_TEXT
    else:
        text = hello_message.message
    if client is None:
        ClientDao.create(
            id=chat_id,
            username=username,
            date_create=date.today(),
        )
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=create_start_keyboard_down()
    )

    all_document = BinaryDocumentDAO.find_all(status_file=Status.FREE.value)
    for document in all_document:
        file_name = f"{document.name}.{document.expansion}"
        file_like = io.BytesIO(document.file_data)
        file_like.name = file_name
        input_file = BufferedInputFile(file=file_like.read(), filename=file_name)
        await bot.send_document(chat_id=chat_id, document=input_file)


async def send_invoice_message(chat_id, bot: Bot, price):
    price_label = types.LabeledPrice(label="Подписка на 1 месяц", amount=price * 100)  # в копейках
    await bot.send_invoice(
        chat_id,
        title="Подписка на канал",
        description="Активация подписки на канал.",
        provider_token=APP_SETTINGS.PAYMENTS_TOKEN_TEST,
        currency="rub",
        is_flexible=False,
        prices=[price_label, ],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )


@user_private_router.message(F.successful_payment)
async def successful_payment(message: types.Message, bot: Bot):
    pyind_praise = message.successful_payment.total_amount / 100
    pay = PaySettingsDAO.find_one_or_none(price=pyind_praise)
    if pay is None:
        await message.answer(
            "Что-то идет не так. Оплата прошла но я не могу понять куда выдать доступ. "
            "Пожалуйста свяжитесь с нами воспользовавшись кнопкой 'Помощь'"
        )
        _help = HelloMessageDAO.find_one_or_none(user_friendly_id=1)
        if _help:
            await bot.send_message(
                chat_id=_help.message,
                text=f"Что-то идет не так с выдачей ссылки на канал, "
                     f"клиенту: @{message.from_user.username}.\n tg_id: {message.chat.id} "
                     "Оплата прошла но похоже стоимость была изменены в админке"
            )
        return
    if pay.user_friendly_id == 1:
        ClientDao.update(
            row_id=message.chat.id,
            is_paid_cheap_content=True,
            date_paid=date.today(),
            # time_paid=datetime.time(datetime.now())
        )
    elif pay.user_friendly_id == 2:
        ClientDao.update(
            row_id=message.chat.id,
            is_paid_expensive_content=True,
            date_paid=date.today(),
            # time_paid=datetime.time(datetime.now())
        )
    else:
        _help = HelloMessageDAO.find_one_or_none(user_friendly_id=1)
        text = (f"Что-то идет не так с выдачей ссылки на канал, "
                f"клиенту: @{message.from_user.username}.\n tg_id: {message.chat.id} "
                "Оплата прошла но похоже в админке нет нужного УНИКАЛЬНОГО ИДЕНТИФИКАТОРА, ДОПУСТИМЫЕ ЗНАЧЕНИЯ 1 ИЛИ 2")
        if _help:
            await bot.send_message(
                chat_id=_help.message,
                text=text
            )
        else:
            await bot.send_message(
                chat_id="324302243",
                text=text
            )

    await message.answer(
        text=f"Платеж прошел успешно!!!\n"
             f"Спасибо за подписку! <a href='{pay.url}'>Вот ссылка на наш канал!</a>"
    )


@user_private_router.message(F.text == "Помощь")
async def keyboard_reaction(message: Message):
    _help = HelpChatDAO.find_one_or_none(user_friendly_id=1)
    if _help:
        await message.answer(
            text=f"Наша поддержка поможет вам в случае возникновения проблем с ботом, в чате: "
                 f"{_help.message}"
        )


@user_private_router.message(F.text)
async def keyboard_reaction(message: Message, bot: Bot):
    pay = PaySettingsDAO.find_one_or_none(btn_text=message.text)
    if pay is None:
        await message.answer("Пожалуйста используйте кнопки для навигации")
        return

    await message.answer(
        text=pay.message
    )
    await send_invoice_message(chat_id=message.chat.id, bot=bot, price=pay.price)
