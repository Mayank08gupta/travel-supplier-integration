from fastapi import APIRouter

router = APIRouter(prefix="/nova", tags=["Nova Supplier"])


@router.post("/search")
async def search_hotels():
    return [
        {
            "property_id": "N200",
            "name": "Grand Palace",
            "city": "Delhi",
            "room": "Executive",
            "currency": "USD",
            "amount": {
                "base": 115,
                "fees": 18
            },
            "status": "available",
            "cancel_policy": "Free until 48 hours"
        },
        {
            "property_id": "N201",
            "name": "City Stay",
            "city": "Delhi",
            "room": "Suite",
            "currency": "USD",
            "amount": {
                "base": 150,
                "fees": 25
            },
            "status": "available",
            "cancel_policy": "Free until 24 hours"
        }
    ]