from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100, collation='utf8mb4_unicode_ci'), unique=True, index=True, nullable=False)
    capital = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    population = Column(Integer, nullable=False)
    currency_code = Column(String(10), nullable=True)
    exchange_rate = Column(Float, nullable=True)
    estimated_gdp = Column(Float, nullable=True)
    flag_url = Column(String(255), nullable=True)
    last_refreshed_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AppStatus(Base):
    __tablename__ = "app_status"

    id = Column(Integer, primary_key=True)
    last_refreshed_at = Column(DateTime, nullable=True)