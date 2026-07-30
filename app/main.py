from fastapi import FastAPI
from app.api.cancel import router as cancel_router
from app.api.search import router as search_router
from app.database.database import Base
from app.database.database import engine
from app.suppliers.atlas import router as atlas_router
from app.suppliers.nova import router as nova_router
from app.api.booking import router as booking_router
from app.api.workflow import router as workflow_router
from app.database.database import Base, engine
from app.database import models
from app.api.booking_detail import router as booking_detail_router
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Travel Aggregator API",
    version="1.0"
)
app.include_router(booking_router)
app.include_router(cancel_router)
app.include_router(atlas_router)
app.include_router(nova_router)
app.include_router(search_router)
app.include_router(workflow_router)
app.include_router(booking_detail_router)
@app.get("/")
async def root():
    return {
        "message": "Travel Platform Running"
    }