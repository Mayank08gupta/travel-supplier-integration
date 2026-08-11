import pytest

from app.models.common import AvailabilityStatus, Supplier
from app.models.response import HotelOffer
from app.services.search_service import SearchService


def create_offer(
    supplier,
    property_id,
    property_name,
    total_price,
    availability=AvailabilityStatus.AVAILABLE,
):
    return HotelOffer(
        supplier=supplier,
        property_id=property_id,
        property_name=property_name,
        location="Noida",
        room_type="Deluxe",
        check_in="2026-08-15",
        check_out="2026-08-17",
        currency="INR",
        base_price=total_price - 500,
        taxes=500,
        total_price=total_price,
        cancellation_policy="Free cancellation",
        availability=availability,
    )


class FakeRequest:
    destination = "Noida"
    check_in = "2026-08-15"
    check_out = "2026-08-17"
    guests = 2
    rooms = 1


@pytest.mark.asyncio
async def test_search_filters_unavailable_and_ranks_by_price(monkeypatch):

    atlas_offer = create_offer(
        Supplier.ATLAS,
        "A1",
        "Atlas Grand",
        5000,
    )

    unavailable_offer = create_offer(
        Supplier.ATLAS,
        "A2",
        "Atlas Sold Out",
        3000,
        AvailabilityStatus.SOLD_OUT,
    )

    nova_offer = create_offer(
        Supplier.NOVA,
        "N1",
        "Nova Palace",
        4000,
    )

    async def fake_atlas_search(*args):
        return [atlas_offer, unavailable_offer]

    async def fake_nova_search(*args):
        return [nova_offer]

    monkeypatch.setattr(
        "app.services.search_service.AtlasAdapter.search_hotels",
        fake_atlas_search,
    )

    monkeypatch.setattr(
        "app.services.search_service.NovaAdapter.search_hotels",
        fake_nova_search,
    )

    monkeypatch.setattr(
        "app.services.search_service.save_offer",
        lambda offer: None,
    )

    service = SearchService()

    results = await service.search(FakeRequest())

    assert len(results) == 2
    assert results[0].property_name == "Nova Palace"
    assert results[1].property_name == "Atlas Grand"


@pytest.mark.asyncio
async def test_duplicate_property_keeps_cheaper_offer(monkeypatch):

    atlas_offer = create_offer(
        Supplier.ATLAS,
        "A1",
        "Same Hotel",
        6000,
    )

    nova_offer = create_offer(
        Supplier.NOVA,
        "N1",
        "Same Hotel",
        4500,
    )

    async def fake_atlas_search(*args):
        return [atlas_offer]

    async def fake_nova_search(*args):
        return [nova_offer]

    monkeypatch.setattr(
        "app.services.search_service.AtlasAdapter.search_hotels",
        fake_atlas_search,
    )

    monkeypatch.setattr(
        "app.services.search_service.NovaAdapter.search_hotels",
        fake_nova_search,
    )

    monkeypatch.setattr(
        "app.services.search_service.save_offer",
        lambda offer: None,
    )

    service = SearchService()

    results = await service.search(FakeRequest())

    assert len(results) == 1
    assert results[0].supplier == Supplier.NOVA
    assert results[0].total_price == 4500


@pytest.mark.asyncio
async def test_search_returns_partial_results_when_supplier_fails(monkeypatch):

    atlas_offer = create_offer(
        Supplier.ATLAS,
        "A1",
        "Atlas Grand",
        5000,
    )

    async def fake_atlas_search(*args):
        return [atlas_offer]

    async def fake_nova_search(*args):
        raise Exception("Nova supplier unavailable")

    monkeypatch.setattr(
        "app.services.search_service.AtlasAdapter.search_hotels",
        fake_atlas_search,
    )

    monkeypatch.setattr(
        "app.services.search_service.NovaAdapter.search_hotels",
        fake_nova_search,
    )

    monkeypatch.setattr(
        "app.services.search_service.save_offer",
        lambda offer: None,
    )

    service = SearchService()

    results = await service.search(FakeRequest())

    assert len(results) == 1
    assert results[0].supplier == Supplier.ATLAS