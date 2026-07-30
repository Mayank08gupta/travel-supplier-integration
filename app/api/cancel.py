from fastapi import APIRouter

from temporalio.client import Client


router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)


@router.post("/cancel/{workflow_id}")
async def cancel_booking(workflow_id: str):

    client = await Client.connect(
        "localhost:7233"
    )

    handle = client.get_workflow_handle(
        workflow_id
    )


    await handle.signal(
        "cancel_booking"
    )


    return {
        "workflow_id": workflow_id,
        "status": "CANCELLATION_REQUESTED"
    }