from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase
import user_agents

app = Flask(__name__)

engine = create_engine("sqlite:///users.db",echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id:Mapped[int] = mapped_column(primary_key = True)

# Модель для хранения информации о пользователе
class UserInfo(Base):

    __tablename__ = "users"

    ip_address: Mapped[str]
    user_agent: Mapped[str]
    device_type: Mapped[str]
    os: Mapped[str]
    browser: Mapped[str]

    def __repr__(self):
        return f'<UserInfo {self.ip_address}>'

# Создаем таблицу
Base.metadata.create_all(engine)