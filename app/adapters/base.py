from abc import ABC, abstractmethod
from typing import List

from app.models.response import HotelOffer


class BaseSupplierAdapter(ABC):

    @abstractmethod
    async def search_hotels(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int,
        rooms: int,
    ) -> List[HotelOffer]:
        pass