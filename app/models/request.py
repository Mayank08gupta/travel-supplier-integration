from pydantic import BaseModel


class HotelSearchRequest(BaseModel):
    destination: str
    check_in: str
    check_out: str
    guests: int
    rooms: int


class BookingRequest(BaseModel):
    supplier: str
    property_id: str
    guest_name: str