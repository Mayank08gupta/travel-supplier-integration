from fastapi import APIRouter

router = APIRouter(prefix="/atlas", tags=["Atlas Supplier"])


@router.post("/search")
async def search_hotels():
    return [
        {
            "hotelId": "A100",
            "hotelName": "Grand Palace",
            "location": "Delhi",
            "roomType": "Deluxe",
            "currency": "USD",
            "price": 120,
            "tax": 20,
            "available": True,
            "cancellation": "Free until 24 hours"
        },
        {
            "hotelId": "A101",
            "hotelName": "Royal Inn",
            "location": "Delhi",
            "roomType": "Standard",
            "currency": "USD",
            "price": 90,
            "tax": 15,
            "available": False,
            "cancellation": "Non-refundable"
        }
    ]