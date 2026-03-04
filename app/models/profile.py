from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime

from app.database.database import Base


class ProteinRecord(Base):

    __tablename__ = "protein_records"

    id = Column(Integer, primary_key=True, index=True)

    protein = Column(Float)

    date = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))