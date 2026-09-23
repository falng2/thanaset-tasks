from datetime import datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Slot(Base):
    """Supports: CON-TECH-01, FR-BKG-01, FR-BKG-06."""

    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_date = Column(Date, nullable=False, index=True)
    start_time = Column(String(5), nullable=False)
    package_code = Column(String(50), nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    remaining = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Booking(Base):
    """Supports: FR-BKG-02, FR-BKG-04, IF-HIS-01."""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    hn = Column(String(20), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False, index=True)
    booking_date = Column(Date, nullable=False, index=True)
    queue_no = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    """Supports: DOM-PDPA-01."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    hn = Column(String(20), nullable=False, index=True)
    accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
