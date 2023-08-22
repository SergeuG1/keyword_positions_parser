from datetime import datetime
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql import func


class KeywordProducts(Base):

    __tablename__ = "keywords_products"

    id = Column(Integer, primary_key=True)
    keyword_id = Column(Integer,  nullable=True)
    product_id = Column(Integer, nullable=True)


    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(),
                        nullable=False, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, default=None, nullable=True)
