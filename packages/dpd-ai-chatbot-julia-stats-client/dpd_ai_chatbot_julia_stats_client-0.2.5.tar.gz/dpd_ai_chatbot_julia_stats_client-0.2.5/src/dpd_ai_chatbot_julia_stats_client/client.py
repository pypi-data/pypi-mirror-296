import aiohttp


class Chronicler:
    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
        self.session = aiohttp.ClientSession()

    async def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.api_endpoint}/{endpoint}"
        async with self.session.request(method, url, **kwargs) as response:
            response_data = await response.json()
            response.raise_for_status()
            return response_data

    async def post(self, endpoint: str, data=None):
        """Отправляет POST запрос к указанному endpoint."""
        return await self._request('POST', endpoint, json=data)

    async def close(self):
        """Закрывает сессию."""
        await self.session.close()
