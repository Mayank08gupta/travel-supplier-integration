from temporalio import activity
from app.database.database import SessionLocal
from app.database.models import BookingDB


@activity.defn(name="revalidate_offer")
async def revalidate_offer(booking_id: int):

    print(f"Revalidating booking {booking_id}")

    return True



@activity.defn(name="create_supplier_booking")
async def create_supplier_booking(booking_id: int):

    print(f"Creating supplier booking {booking_id}")

    # Supplier booking simulation
    # Removed random failure for testing stable flow

    return {
        "booking_id": booking_id,
        "supplier_reference": f"SUP-{booking_id}"
    }



@activity.defn(name="save_confirmation")
async def save_confirmation(data: dict):

    print("Saving confirmation:", data)

    db = SessionLocal()

    try:

        booking_id = data["booking_id"]

        booking = db.query(BookingDB).filter(
            BookingDB.id == booking_id
        ).first()


        if booking:

            booking.status = "CONFIRMED"

            # update supplier reference if column exists
            if hasattr(booking, "supplier_reference"):
                booking.supplier_reference = data.get(
                    "supplier_reference"
                )

            db.commit()

            print(
                f"Booking {booking_id} confirmed"
            )

        else:

            print(
                f"Booking {booking_id} not found"
            )


    except Exception as e:

        db.rollback()

        print(
            "Confirmation error:",
            e
        )

        raise e


    finally:

        db.close()


    return True



@activity.defn(name="cancel_supplier_booking")
async def cancel_supplier_booking(booking_id: int):

    print(
        f"Cancelling supplier booking {booking_id}"
    )

    db = SessionLocal()

    try:

        booking = db.query(BookingDB).filter(
            BookingDB.id == booking_id
        ).first()


        if booking:

            booking.status = "CANCELLED"

            db.commit()

            print(
                f"Booking {booking_id} cancelled"
            )

        else:

            print(
                f"Booking {booking_id} not found"
            )


    except Exception as e:

        db.rollback()

        print(
            "Cancellation error:",
            e
        )

        raise e


    finally:

        db.close()


    return {
        "cancelled": True,
        "booking_id": booking_id
    }