import typing
from typing import Optional

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.geocoder.dataclasses import PointCoordinates, PointAddresse

if typing.TYPE_CHECKING:
    from app.web.app import Application


class YandexApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = self.app.config.yandex_api.key

    async def connect(self, app: "Application"):

        self.session = ClientSession()

    async def disconnect(self, app: "Application"):

        if self.session:
            await self.session.close()

    @staticmethod
    def _build_query(key: str, city: str, addresse: str) -> str:
                
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey={key}&geocode={city},{addresse}&results=1&lang=ru_RU&format=json"

        return url
 

    async def get_geo_point(self, addresse: PointAddresse) -> None:
        query = self._build_query(
            key = self.key,
            city=addresse.city,
            addresse=addresse.addresse
        )

        async with self.session.get(query) as response:
            data = await response.json()
            pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()

        return PointCoordinates(float(pos[1]), float(pos[0]))

