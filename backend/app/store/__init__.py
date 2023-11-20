import typing

from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.admin.accessor import AdminAccessor
        from app.store.users.accessor import UserAccessor
        from app.store.users.accessor import UserLoginAccessor
        from app.store.ranks.accessor import RankAccessor
        from app.store.positions.accessor import PositionAccessor
        from app.store.jobs.accessor import JobAccessor
        from app.store.problems.accessor import ProblemAccessor
        from app.store.products.accessor import ProductAccessor
        from app.store.partners.accessor import PartnerAccessor
        from app.store.addresses.accessor import AddresseAccessor
        from app.store.offices.accessor import OfficeAccessor
        from app.store.partner_params.accessor import PartnerParamAccessor
        from app.store.todo.accessor import ToDoAccessor
        from app.store.geocoder.accessor import YandexApiAccessor

        self.admins = AdminAccessor(app)
        self.users = UserAccessor(app)
        self.user_logins = UserLoginAccessor(app)
        self.ranks = RankAccessor(app)
        self.positions = PositionAccessor(app)
        self.problems = ProblemAccessor(app)
        self.products = ProductAccessor(app)
        self.partners = PartnerAccessor(app)
        self.jobs = JobAccessor(app)
        self.addresses = AddresseAccessor(app)
        self.offices = OfficeAccessor(app)
        self.geocoder = YandexApiAccessor(app)
        self.partner_params = PartnerParamAccessor(app)
        self.todo = ToDoAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
