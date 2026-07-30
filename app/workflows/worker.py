import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from app.workflows.booking_workflow import BookingWorkflow
from app.activities.booking_activities import (
    revalidate_offer,
    create_supplier_booking,
    save_confirmation,
    cancel_supplier_booking,
)


async def main():

    client = await Client.connect(
        "localhost:7233"
    )

    worker = Worker(
        client,
        task_queue="booking-task-queue",
        workflows=[
            BookingWorkflow
        ],
        activities=[
            revalidate_offer,
            create_supplier_booking,
            save_confirmation,
            cancel_supplier_booking,
        ],
    )

    print("Worker started")

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())