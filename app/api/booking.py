from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from temporalio.client import Client

from app.database.database import get_db
from app.database.models import BookingDB


router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)


@router.post("/")
async def create_booking(
    data: dict,
    db: Session = Depends(get_db)
):

    booking = BookingDB(
        supplier=data["supplier"],
        property_id=data["property_id"],
        guest_name=data["guest_name"],
        status="WORKFLOW_STARTED"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)


    workflow_id = f"booking-{booking.id}"


    booking.workflow_id = workflow_id

    db.commit()


    client = await Client.connect(
        "localhost:7233"
    )


    await client.start_workflow(
        "BookingWorkflow",
        booking.id,
        id=workflow_id,
        task_queue="booking-task-queue"
    )


    return {
        "booking_id": booking.id,
        "workflow_id": workflow_id,
        "status": "WORKFLOW_STARTED"
    }