from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime

from app.database.database import Base


class HotelOfferDB(Base):

    __tablename__ = "hotel_offers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    supplier = Column(String)

    property_id = Column(String)

    property_name = Column(String)

    location = Column(String)

    room_type = Column(String)

    check_in = Column(String)

    check_out = Column(String)

    currency = Column(String)

    base_price = Column(Float)

    taxes = Column(Float)

    total_price = Column(Float)

    cancellation_policy = Column(String)

    availability = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class BookingDB(Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_id = Column(
        String,
        unique=True,
        index=True
    )

    supplier = Column(String)

    property_id = Column(String)

    guest_name = Column(String)

    status = Column(
        String,
        default="STARTED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )