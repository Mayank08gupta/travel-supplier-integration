from pydantic import BaseModel


class BookingRequest(BaseModel):
    property_id: str
    supplier: str
    guest_name: str


class BookingResponse(BaseModel):
    booking_id: str
    supplier_reference: str
    status: str