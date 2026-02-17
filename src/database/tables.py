"""Module for defining the database tables."""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, UUID, Text

from src.database.database import Base


class AccessGroups(Base):
    """The acess groups table structure."""

    __tablename__ = "access_groups"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)


class Jwts(Base):
    """The jwt tokens table structure."""

    __tablename__ = "jwts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    access_group = Column(
        UUID(as_uuid=True), ForeignKey("access_groups.id"), nullable=False
    )
    signature = Column(Text, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    date_created = Column(DateTime, nullable=False)
    last_refresh = Column(DateTime, nullable=True)
    times_refreshed = Column(Integer, nullable=False, default=0)

    access_group_rel = relationship("access_groups", foreign_keys="access_group")


access_groups_table = AccessGroups.__table__
jwts_table = Jwts.__table__
