from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import BookingDB


router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(BookingDB).filter(
        BookingDB.id == booking_id
    ).first()


    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )


    return {
        "id": booking.id,
        "workflow_id": booking.workflow_id,
        "supplier": booking.supplier,
        "property_id": booking.property_id,
        "guest_name": booking.guest_name,
        "status": booking.status
    }