from datetime import datetime
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql import func


class KeywordPositions(Base):

    __tablename__ = "keywords_positions"

    id = Column(Integer, primary_key=True)
    product_id = Column(String, nullable=True)
    keyword_id = Column(Integer, nullable=True)

    page = Column(String, nullable=True)
    position = Column(Integer, nullable=True)
    date = Column(TIMESTAMP, default=None, nullable=True)
    
    
    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(),
                        nullable=False, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, default=None, nullable=True)

