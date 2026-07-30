from pydantic import BaseModel

from app.models.common import AvailabilityStatus, Supplier


class HotelOffer(BaseModel):

    supplier: Supplier

    property_id: str

    property_name: str

    location: str

    room_type: str

    check_in: str

    check_out: str

    currency: str

    base_price: float

    taxes: float

    total_price: float

    cancellation_policy: str

    availability: AvailabilityStatus