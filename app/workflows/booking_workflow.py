from datetime import timedelta

from temporalio import workflow


@workflow.defn
class BookingWorkflow:

    def __init__(self):
        self.status = "STARTED"
        self.cancel_requested = False


    @workflow.run
    async def run(self, booking_id: int):

        # Step 1: Validate booking
        self.status = "VALIDATING"

        await workflow.execute_activity(
            "revalidate_offer",
            booking_id,
            start_to_close_timeout=timedelta(seconds=10),
        )


        # Step 2: Create supplier reservation
        self.status = "CREATING_RESERVATION"

        reservation = await workflow.execute_activity(
            "create_supplier_booking",
            booking_id,
            start_to_close_timeout=timedelta(seconds=20),
        )


        # Step 3: Save confirmation in database
        await workflow.execute_activity(
            "save_confirmation",
            reservation,
            start_to_close_timeout=timedelta(seconds=10),
        )


        self.status = "CONFIRMED"


        # Wait for cancellation signal
        await workflow.wait_condition(
            lambda: self.cancel_requested
        )


        # Cancellation flow
        self.status = "CANCELLING"


        await workflow.execute_activity(
            "cancel_supplier_booking",
            booking_id,
            start_to_close_timeout=timedelta(seconds=10),
        )


        self.status = "CANCELLED"


        return {
            "booking_id": booking_id,
            "status": self.status
        }



    @workflow.signal(name="cancel_booking")
    def cancel_booking(self):

        self.cancel_requested = True



    @workflow.query(name="get_status")
    def get_status(self):

        return self.status