from sqlalchemy import select, insert, update, create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Client, BinaryDocument, PaySettings, HelloMessage, HelpChat
from src.settings import APP_SETTINGS

engine = create_engine(APP_SETTINGS.DB_URL, echo=False)

Session = sessionmaker(autoflush=False, bind=engine)


class BaseDAO:
    model: Base | None = None

    @classmethod
    def find_by_id(cls, model_id: int):
        with Session() as session:
            q = select(cls.model).filter_by(id=model_id)
            result = session.execute(q)
            return result.scalar_one_or_none()

    @classmethod
    def find_one_or_none(cls, **kwargs):
        with Session() as session:
            q = select(cls.model).filter_by(**kwargs)
            result = session.execute(q)
            return result.scalar_one_or_none()

    @classmethod
    def find_all(cls, **kwargs):
        with Session() as session:
            q = select(cls.model).filter_by(**kwargs)
            result = session.execute(q)
            return result.scalars().all()

    @classmethod
    def create(cls, **data):
        with Session() as session:
            q = insert(cls.model).values(**data)
            session.execute(q)
            session.commit()


class ClientDao(BaseDAO):
    model = Client

    @classmethod
    def update(cls, row_id: int, **data):
        with Session() as session:
            q = (
                update(cls.model)
                .where(cls.model.id == row_id)
                .values(**data)
            )
            session.execute(q)
            session.commit()


class BinaryDocumentDAO(BaseDAO):
    model = BinaryDocument


class PaySettingsDAO(BaseDAO):
    model = PaySettings


class HelloMessageDAO(BaseDAO):
    model = HelloMessage


class HelpChatDAO(BaseDAO):
    model = HelpChat
