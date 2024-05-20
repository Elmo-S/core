"""Library for HSL API."""

from datetime import datetime
import aiohttp

from .const import API_URL


class HSL:
    """Class for handling API calls and validation."""

    def __init__(self, api_key, session: aiohttp.ClientSession) -> None:
        """Initialize API instance."""
        self.url = API_URL

        self.api_key = api_key
        self._session = session
        self.header = {
            "content-type": "application/json",
            "digitransit-subscription-key": "c61f2289a9d9496dbe1e8cb88e909e67",
        }

    async def post(self, query: str):
        """Make API call."""
        response = await self._session.post(
            self.url, json={"query": query}, headers=self.header
        )
        return response

    async def authenticate(self) -> int:
        """Authenticate API connection."""
        query = """{stop(id: "HSL:1140447") {name}}"""
        response = await self.post(query)
        return response.status

    async def fetch_data(self) -> str:
        """Fetch data."""
        query = """{
            stop(id: "HSL:1140447") {
                name
                stoptimesWithoutPatterns{
                    scheduledArrival
                    realtimeArrival
                    realtime
                    realtimeState
                    serviceDay
                    headsign
                    trip{
                        route{
                            shortName
                            mode
                        }
                    }
                }
            }
        }"""
        response = await self.post(query)
        response = await response.json()

        service_day = response["data"]["stop"]["stoptimesWithoutPatterns"][0][
            "serviceDay"
        ]
        realtime_arrival = response["data"]["stop"]["stoptimesWithoutPatterns"][0][
            "realtimeArrival"
        ]

        timestamp = service_day + realtime_arrival
        arrival_time = datetime.fromtimestamp(timestamp)

        current_time = datetime.now()

        difference = arrival_time - current_time

        minutes = divmod(difference.total_seconds(), 60)[0]

        response["data"]["stop"]["stoptimesWithoutPatterns"][0][
            "arrival_time"
        ] = arrival_time.isoformat()
        response["data"]["stop"]["stoptimesWithoutPatterns"][0]["timestamp"] = minutes

        return response["data"]
