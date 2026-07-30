import uuid

from app.database.database import SessionLocal
from app.database.models import BookingDB
from app.database.models import HotelOfferDB


def save_offer(offer):

    db = SessionLocal()

    row = HotelOfferDB(
        supplier=offer.supplier.value,
        property_id=offer.property_id,
        property_name=offer.property_name,
        location=offer.location,
        room_type=offer.room_type,
        currency=offer.currency,
        total_price=offer.total_price,
        availability=offer.availability.value,
    )

    db.add(row)

    db.commit()

    db.close()


def create_booking(data):

    db = SessionLocal()

    booking = BookingDB(
        supplier=data["supplier"],
        property_id=data["property_id"],
        guest_name=data["guest_name"],
        booking_reference=str(uuid.uuid4()),
        status="pending",
    )

    db.add(booking)

    db.commit()

    db.refresh(booking)

    db.close()

    return booking