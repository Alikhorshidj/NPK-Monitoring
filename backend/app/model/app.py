from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    func,
    Integer,
    DateTime,
    ForeignKey,
)
from core.database import Base
from sqlalchemy.orm import relationship

class LandModel(Base):
    __tablename__ = "land"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    landname = Column(String(250), nullable=False, unique=False)
    group_id = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)

    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    user = relationship("UserModel", back_populates="land", uselist=False)
