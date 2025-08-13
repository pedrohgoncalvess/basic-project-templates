from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, func, UUID, Boolean

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Cep(Base):
    __tablename__ = 'cep'
    __table_args__ = {'schema': 'example'}

    id = Column(Integer, primary_key=True)
    cep = Column(String(8), nullable=False, unique=True)
    logradouro = Column(String(250))
    bairro = Column(String(150))
    cidade = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)