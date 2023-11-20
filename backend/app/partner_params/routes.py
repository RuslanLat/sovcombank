import typing

from app.partner_params.views import (
    PartnerParamAddView,
    PartnerParamListView,
    PartnerParamDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/partner.param.add", PartnerParamAddView)
    app.router.add_view("/partner.param.delete", PartnerParamDeleteView)
    app.router.add_view("/partner.param.list", PartnerParamListView)