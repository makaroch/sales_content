from aiogram import Router, F, Bot
from aiogram.types import ChatJoinRequest

from src.handlers.user_private import start_message
from src.database.dao import ClientDao, PaySettingsDAO, HelloMessageDAO

user_channel_router = Router()


@user_channel_router.chat_join_request()
async def join_request_handler(chat_join_request: ChatJoinRequest, bot: Bot) -> None:
    chanel_id = chat_join_request.chat.id
    user = ClientDao.find_one_or_none(id=chat_join_request.from_user.id)
    pay = PaySettingsDAO.find_one_or_none(id_chanel=chanel_id)
    if pay is None:
        _help = HelloMessageDAO.find_one_or_none(user_friendly_id=1)
        text = (f"Что-то идет не так с подтверждением доступа для "
                f"клиента: @{chat_join_request.from_user.username}.\n tg_id: {chat_join_request.chat.id} "
                f"Он ломиться в чат с id {chanel_id} но в базе такого нет")
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

        return
    if user is None:
        await start_message(
            chat_id=chat_join_request.from_user.id,
            bot=bot,
            username=chat_join_request.from_user.username
        )
        return

    if pay.user_friendly_id == 1:
        is_paid = user.is_paid_cheap_content
    elif pay.user_friendly_id == 2:
        is_paid = user.is_paid_expensive_content
    else:
        _help = HelloMessageDAO.find_one_or_none(user_friendly_id=1)
        text = (f"Что-то идет не так с подтверждением  доступа в канал, "
                f"клиенту: @{chat_join_request.from_user.username}.\n tg_id: {chat_join_request.chat.id} "
                "Похоже в админке нет нужного УНИКАЛЬНОГО ИДЕНТИФИКАТОРА, ДОПУСТИМЫЕ ЗНАЧЕНИЯ 1 ИЛИ 2")
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
        return
    if not is_paid:
        await start_message(
            chat_id=chat_join_request.from_user.id,
            bot=bot,
            username=chat_join_request.from_user.username
        )
        return
    await chat_join_request.approve()
