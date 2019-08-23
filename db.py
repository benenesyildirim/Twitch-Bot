from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Bot(Base):
    __tablename__ = 'tb_command'

    id = Column(Integer, primary_key=True)
    command = Column(String(250), nullable=False)
    response = Column(String(1000), nullable=False)


engine = create_engine('sqlite:///bot.db')

Base.metadata.create_all(engine)
