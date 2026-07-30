from fastapi import APIRouter

from app.models.request import HotelSearchRequest
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Unified Search"]
)


@router.post("/hotels")
async def search_hotels(request: HotelSearchRequest):

    service = SearchService()

    return await service.search(request)