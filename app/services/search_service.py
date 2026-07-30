from app.adapters.atlas_adapter import AtlasAdapter
from app.adapters.nova_adapter import NovaAdapter
from app.database.crud import save_offer
import asyncio


class SearchService:

    async def search(self, request):

        atlas = AtlasAdapter()
        nova = NovaAdapter()

        atlas_task = atlas.search_hotels(
            request.destination,
            request.check_in,
            request.check_out,
            request.guests,
            request.rooms,
        )

        nova_task = nova.search_hotels(
            request.destination,
            request.check_in,
            request.check_out,
            request.guests,
            request.rooms,
        )

        atlas_results, nova_results = await asyncio.gather(
            atlas_task,
            nova_task,
            return_exceptions=True,
        )

        offers = []

        if not isinstance(atlas_results, Exception):
            offers.extend(atlas_results)

        if not isinstance(nova_results, Exception):
            offers.extend(nova_results)

        offers = [
            o
            for o in offers
            if o.availability.value == "available"
        ]

        unique = {}

        for offer in offers:

            key = offer.property_name.lower()

            if key not in unique:
                unique[key] = offer

            elif offer.total_price < unique[key].total_price:
                unique[key] = offer

        ranked = sorted(
            unique.values(),
            key=lambda x: x.total_price,
        )

        for offer in ranked:
            save_offer(offer)

        return ranked