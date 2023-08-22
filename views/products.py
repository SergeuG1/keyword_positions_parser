from datetime import datetime
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=True)

    name = Column(String, nullable=True)
    link_on_site = Column(String, nullable=True)
    hasNote = Column(Boolean, nullable=True)
    article_china = Column(String, nullable=True)
    wb_article = Column(Integer, nullable=True)
    nomenclature = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    default_image_url = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow(),
                        nullable=False, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, default=None, nullable=True)
