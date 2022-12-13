"""Library for HSL API."""
import aiohttp

from .const import API_URL


class HSL:
    """Class for handling API calls and validation."""

    def __init__(self, api_key, session: aiohttp.ClientSession) -> None:
        """Initialize API instance."""
        self.url = API_URL
        self.header = {"content-type": "application/json"}
        self.api_key = api_key
        self._session = session

    async def post(self, query: str):
        """Make API call."""
        response = await self._session.post(
            self.url, json={"query": query}, headers=self.header
        )
        return response

    async def authenticate(self) -> bool:
        """Authenticate API connection."""
        query = """{stop(id: "HSL:1140447") {name}}"""
        response = await self.post(query)
        if not response.status == 200:
            return False
        return True

    async def fetch_data(self) -> str:
        """Fetch data."""
        return "Buuuuuuip"
