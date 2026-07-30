import httpx

from app.adapters.base import BaseSupplierAdapter
from app.models.common import AvailabilityStatus, Supplier
from app.models.response import HotelOffer


class AtlasAdapter(BaseSupplierAdapter):

    async def search_hotels(
        self,
        destination,
        check_in,
        check_out,
        guests,
        rooms,
    ):

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8000/atlas/search"
            )

        hotels = response.json()

        offers = []

        for hotel in hotels:

            offers.append(
                HotelOffer(
                    supplier=Supplier.ATLAS,
                    property_id=hotel["hotelId"],
                    property_name=hotel["hotelName"],
                    location=hotel["location"],
                    room_type=hotel["roomType"],
                    check_in=check_in,
                    check_out=check_out,
                    currency=hotel["currency"],
                    base_price=hotel["price"],
                    taxes=hotel["tax"],
                    total_price=hotel["price"] + hotel["tax"],
                    cancellation_policy=hotel["cancellation"],
                    availability=(
                        AvailabilityStatus.AVAILABLE
                        if hotel["available"]
                        else AvailabilityStatus.SOLD_OUT
                    ),
                )
            )

        return offers