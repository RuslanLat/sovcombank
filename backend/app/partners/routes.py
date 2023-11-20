import typing

from app.partners.views import (
    PartnerAddView,
    PartnerListView,
    PartnerUpdateView,
    PartnerDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/partner.add", PartnerAddView)
    app.router.add_view("/partner.update", PartnerUpdateView)
    app.router.add_view("/partner.delete", PartnerDeleteView)
    app.router.add_view("/partner.list", PartnerListView)