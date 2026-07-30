from fastapi import APIRouter

from temporalio.client import Client


router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"]
)


@router.get("/{workflow_id}")
async def get_workflow_status(workflow_id: str):

    client = await Client.connect(
        "localhost:7233"
    )

    handle = client.get_workflow_handle(
        workflow_id
    )

    result = await handle.query(
        "get_status"
    )

    return {
        "workflow_id": workflow_id,
        "status": result
    }