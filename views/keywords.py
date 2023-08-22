from datetime import datetime
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func


class Keywords(Base):

    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(),
                        nullable=False, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, default=None, nullable=True)
