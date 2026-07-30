import httpx

from app.adapters.base import BaseSupplierAdapter
from app.models.common import AvailabilityStatus, Supplier
from app.models.response import HotelOffer


class NovaAdapter(BaseSupplierAdapter):

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
                "http://127.0.0.1:8000/nova/search"
            )

        hotels = response.json()

        offers = []

        for hotel in hotels:

            offers.append(
                HotelOffer(
                    supplier=Supplier.NOVA,
                    property_id=hotel["property_id"],
                    property_name=hotel["name"],
                    location=hotel["city"],
                    room_type=hotel["room"],
                    check_in=check_in,
                    check_out=check_out,
                    currency=hotel["currency"],
                    base_price=hotel["amount"]["base"],
                    taxes=hotel["amount"]["fees"],
                    total_price=hotel["amount"]["base"] + hotel["amount"]["fees"],
                    cancellation_policy=hotel["cancel_policy"],
                    availability=(
                        AvailabilityStatus.AVAILABLE
                        if hotel["status"] == "available"
                        else AvailabilityStatus.SOLD_OUT
                    ),
                )
            )

        return offers