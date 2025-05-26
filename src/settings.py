from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class AppSettings:
    """
        Application settings
    """
    TG_BOT_TOKEN = getenv("TG_BOT_TOKEN", None)
    PAYMENTS_TOKEN_TEST = getenv("PAYMENTS_TOKEN_TEST", None)
    PAYMENTS_TOKEN = getenv("PAYMENTS_TOKEN", None)

    POSTGRES_DB = getenv("POSTGRES_DB", None)
    POSTGRES_USER = getenv("POSTGRES_USER", None)
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", None)
    POSTGRES_HOST = getenv("POSTGRES_HOST", None)
    POSTGRES_PORT = getenv("POSTGRES_PORT", None)
    DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    ADMIN_GROUP_ID = getenv("ADMIN_GROUP_ID", None)
    CHANNEL_URL1 = getenv("CHANNEL_URL_2000", None)
    CHANNEL_URL2 = getenv("CHANNEL_URL_5000", None)
    FILE_NAME = "content.zip"

    HELLO_TEXT = (
        "Привет!\n"
        "Ты только что открыл дверь в мир, где искусственный интеллект работает на тебя.\n"
        "🎁Держи свой персональный подарок «GPT-Старт: 10+ Запросов для Результата Сегодня». 🚀\n"
        "📄 Внутри – готовые запросы для мгновенной пользы. Скопируй, вставь и получи результат!\n"
        "Это твой быстрый старт. \n"
        "А когда освоишься, подумай, что тебе интереснее: стать профи в общении с GPT для любых задач или научиться"
        " создавать с помощью ИИ крутой видеоконтент? 😉 Скоро расскажу, как это сделать!\n"
        "Открывай файл и тестируй запросы прямо сейчас! "
    )

    PRICE1 = 2000
    PRICE2 = 5000

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        for key, value in self.__dict__.items():
            if value is None:
                raise ValueError(f"Environment variable {key} is not set")


APP_SETTINGS = AppSettings()
